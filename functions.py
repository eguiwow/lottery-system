from datetime import datetime, timedelta
from typing import List
from sqlalchemy import DateTime, func, select
from sqlalchemy.exc import IntegrityError
from models import User, Lottery, Ballot
import random as rand
from schedule import every, repeat
import time
from __init__ import session

import logging

logging.basicConfig(level=logging.INFO)

def register_user(session, username: str, password: str):
    """Register a new user"""
    user = User(username=username, password=password)
    # Check if a user with the same name already exists
    try:
        # Add the new user to the session and commit the changes
        session.add(user)
        session.commit()
        print("New user created successfully!")
    except IntegrityError as e:
        session.rollback()
        logging.warning(f"{e.orig}: A user with the same name already exists!")

def create_lottery(session, name: str, closing_date: DateTime):
    """Create a new lottery"""
    lottery = Lottery(name=name, closing_date=closing_date)
    try:
        # Add the new user to the session and commit the changes
        session.add(lottery)
        session.commit()
        logging.info("New lottery created successfully!")
    except IntegrityError as e:
        session.rollback()
        logging.warning(f"{e.orig}: A lottery in the same date already exists!")

def submit_ballot_id(session, user_id: int, lottery_id: int):
    """Submit a ballot for a specific lottery and user providing both IDs"""
    lottery = session.query(Lottery).get(lottery_id)

    if lottery.closing_date < datetime.now():
        logging.info("This lottery has already closed.")
        return

    ballot = Ballot(user_id=user_id, lottery_id=lottery_id)
    session.add(ballot)
    session.commit()
    logging.info("Ballot submitted successfully.")

def submit_ballot_date(session, username: str, lottery_date: DateTime):
    """Submit a ballot for a specific lottery-date and a given username"""
    lottery = session.query(Lottery).filter(Lottery.closing_date == lottery_date).first()
    user = session.query(User).filter(User.username==username).first()
    if lottery:
        if user:
            if lottery.closing_date < datetime.now():
                logging.info("This lottery has already closed.")
                return
            ballot = Ballot(user_id=user.user_id, lottery_id=lottery.id)
            session.add(ballot)
            session.commit()
            logging.info("Ballot submitted successfully.")
        else:
            logging.info(f"The requested user {user.username} does not exist.")            
    else:
        logging.info(f"The requested lottery for date {lottery_date} does not exist.")

def close_open_lotteries(session):
    """Close open lotteries and select random winners"""
    open_lotteries = session.query(Lottery).filter(Lottery.closing_date <= datetime.now()).filter(Lottery.winning_ballot_id == None )

    not_closed = 0 # if a lottery is not closed, don't display the success message
    if open_lotteries.all():
        for lottery in open_lotteries.all():
            if lottery.winning_ballot_id is None:
                # random ballot selected as winner
                ballot = session.query(Ballot).filter(Ballot.lottery == lottery).order_by(func.random()).first()
                if ballot:           
                    lottery.winning_ballot_id = ballot.id
                    session.commit()
                else:
                    logging.info(f"No ballots found for lottery {str(lottery.closing_date)}")
                    not_closed = 1
            else:
                winning_ballot = session.query(Ballot).get(lottery.winning_ballot_id)
                logging.info(f"The winning ballot for {str(lottery.closing_date)[0:10]} lottery was submitted by user: {winning_ballot.user.username}")
        if not_closed == 0:
            logging.info("Lotteries closed successfully.")
    else:
        logging.info("All lotteries are closed right now")
    

def check_winning_ballot_by_lottery_id(session, lottery_id: int):
    """Check the winning ballot for a specific lottery"""
    lottery = session.query(Lottery).get(lottery_id)

    if lottery.winning_ballot_id is None:
        logging.info("No winning ballot found for this lottery.")
    else:
        winning_ballot = session.query(Ballot).get(lottery.winning_ballot_id)
        logging.info(f"The winning ballot for this lottery is submitted by user: {winning_ballot.user.username}")


def check_winning_ballot_by_date(session, lottery_date: DateTime):
    """Check the winning ballot for a specific lottery"""
    lottery = session.query(Lottery).filter(Lottery.closing_date == lottery_date).first()
    if lottery:
        if lottery.winning_ballot_id is None:
            logging.info("No winning ballot found for this lottery.")
        else:
            winning_ballot = session.query(Ballot).filter(Ballot.id==lottery.winning_ballot_id).first()
            logging.info(f"The winning ballot for the {lottery_date} lottery is submitted by user: {winning_ballot.user.username}")
    else:
        logging.info(f"The consulted lottery for date {lottery_date} does not exist.")

def close_lottery_and_select_winner(session, closing_time: DateTime, minute: bool):
    """Close the lottery at closing_time and select a random winner"""
    time.sleep(1)
    current_time = datetime.now()
    if current_time >= closing_time:
        # Past midnight so we close the lottery and declare a winner
        close_open_lotteries(session)
        if minute:
            last_minute = datetime.now().replace(second=0, microsecond=0) - timedelta(minutes=1)
            # Check the winner from last minute
            check_winning_ballot_by_date(session, last_minute)
        else:
            yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
            # Check the winner from yesterday
            check_winning_ballot_by_date(session, yesterday)


# SCHEDULING for midnight closing of lottery 
def do_at_midnight():
    """Schedule the next run of the lottery event at midnight"""
    closing_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    next_run_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    close_lottery_and_select_winner(session, closing_time, minute=False)
    create_lottery(session, "Loto" + str(next_run_time)[0:10], next_run_time)
    logging.info(f"Next run scheduled for: {str(next_run_time)[0:10]}")

# SCHEDULING for minute closing of lottery
def do_every_minute():
    """Schedule the next run of the lottery event every minute"""
    closing_time = datetime.now().replace(second=0, microsecond=0)
    next_run_time = datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=1)
    close_lottery_and_select_winner(session, closing_time, minute=True)
    create_lottery(session, "Loto" + str(next_run_time), next_run_time)
    # Random ballots to test your fortune against
    submit_random_ballots(session, next_run_time, 10)
    logging.info(f"Next run scheduled for: {next_run_time}")

def schedule_midnight():
    every().day.at("00:00").do(do_at_midnight)

def schedule_minute():
    every().minute.at(":00").do(do_every_minute)

# DB populating related functions 
# -------------------------------

# We get rid of the date constraint to populate the db
def submit_past_ballot(session, user_id: int, lottery_id: int):
    """Submit a ballot for a specific lottery (opened or closed)"""
    lottery = session.query(Lottery).get(lottery_id)
    user = session.query(User).get(user_id)
    ballot = Ballot(user_id=user_id, lottery_id=lottery_id)
    session.add(ballot)
    session.commit()
    logging.debug(f"Ballot from {user.username} submitted successfully to lottery from {lottery.closing_date}.")


def submit_random_ballots(session, lottery_date, num_random_ballots):
    lottery = session.query(Lottery).filter(Lottery.closing_date == lottery_date).first()
    if lottery:
        count = session.execute(func.count(User.id)).scalar()
        for i in range(num_random_ballots):
            ballot = Ballot(user_id=rand.randint(1, count), lottery_id=lottery.id)
            session.add(ballot)
        session.commit()
        logging.debug(f"Ballots from random users submitted successfully to lottery from {lottery.closing_date}.")
    else:
        logging.info(f"The requested lottery for date {lottery_date} does not exist.")

def populate_db(session, origin_date: DateTime):
    """Populate the database with test data"""
    # Sample list of names from where to create users
    names = ["Frodo", "Legolas", "Aragorn", "Gandalf", "Gimli", "Pippin", "Merry", "Sam", "Boromir"]
    
    # Get the current date
    current_date = datetime.now().date()

    # Calculate the number of days that have passed
    days_passed = (current_date - origin_date.date()).days

    # Populate the db with users from list and passwords
    for name in names:
        for i in range(1, 10):
            register_user(session, name+str(i), "pass"+str(i))
    # Populate the db with a new lottery each day since origin_date
    for i in range(days_passed + 1):
        new_date = origin_date + timedelta(i)
        create_lottery(session, "Loto" + str(new_date)[0:10], new_date)
    
    num_lotteries = session.query(Lottery.id).count()
    num_users = session.query(User.id).count()    
    # Submit ballots from random users to random lotteries
    for i in range(1000):
        submit_past_ballot(session, rand.randint(1, num_users), rand.randint(1, num_lotteries))

    close_open_lotteries(session)

def test_db():
    # Example usage
    register_user("HarryPotter", "pass123")
    register_user("HermioneGranger", "pass456")
    create_lottery("LaLoto", datetime(2023,1, 22))
    submit_ballot_id(1, 1)
    submit_ballot_id(2, 1)
    submit_ballot_id(1, 1)


