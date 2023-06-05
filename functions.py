from datetime import datetime, timedelta
from typing import List
from sqlalchemy import DateTime, func
from sqlalchemy.exc import IntegrityError
from models import User, Lottery, Ballot
import random as rand
from schedule import every, repeat
import time
from __init__ import session

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
        print(f"{e.orig}: A user with the same name already exists!")

def create_lottery(session, name: str, closing_date: DateTime):
    """Create a new lottery"""
    lottery = Lottery(name=name, closing_date=closing_date)

    try:
        # Add the new user to the session and commit the changes
        session.add(lottery)
        session.commit()
        print("New lottery created successfully!")
    except IntegrityError as e:
        session.rollback()
        print(f"{e.orig}: A lottery in the same date already exists!")

def submit_ballot(session, user_id: int, lottery_id: int):
    """Submit a ballot for a specific lottery"""
    lottery = session.query(Lottery).get(lottery_id)

    if lottery.closing_date < datetime.now():
        print("This lottery has already closed.")
        return

    ballot = Ballot(user_id=user_id, lottery_id=lottery_id)
    session.add(ballot)
    session.commit()
    print("Ballot submitted successfully.")

def close_open_lotteries(session):
    """Close open lotteries and select random winners"""
    open_lotteries = session.query(Lottery).filter(Lottery.closing_date <= datetime.now()).filter(Lottery.winning_ballot_id == None )

    time.sleep(2)

    if open_lotteries.all():
        for lottery in open_lotteries.all():
            if lottery.winning_ballot_id is None:
                # random ballot selected as winner
                ballot = session.query(Ballot).filter(Ballot.lottery == lottery).order_by(func.random()).first()
                if ballot:           
                    lottery.winning_ballot_id = ballot.id
                    session.commit()
                else:
                    print(f"No ballots found for lottery {str(lottery.closing_date)[0:10]}")
            else:
                winning_ballot = session.query(Ballot).get(lottery.winning_ballot_id)
                print(f"The winning ballot for {str(lottery.closing_date)[0:10]} lottery was submitted by user: {winning_ballot.user.username}")
        print("Lotteries closed successfully.")
    else:
        print("All lotteries are closed right now")
    

def check_winning_ballot_by_lottery_id(session, lottery_id: int):
    """Check the winning ballot for a specific lottery"""
    lottery = session.query(Lottery).get(lottery_id)

    if lottery.winning_ballot_id is None:
        print("No winning ballot found for this lottery.")
    else:
        winning_ballot = session.query(Ballot).get(lottery.winning_ballot_id)
        print(f"The winning ballot for this lottery is submitted by user: {winning_ballot.user.username}")


def check_winning_ballot_by_date(session, lottery_date: DateTime):
    """Check the winning ballot for a specific lottery"""
    lottery = session.query(Lottery).filter(Lottery.closing_date == lottery_date).first()
    print(lottery.closing_date)
    if lottery.winning_ballot_id is None:
        print("No winning ballot found for this lottery.")
    else:
        winning_ballot = session.query(Ballot).filter(Ballot.id==lottery.winning_ballot_id).first()
        print(f"The winning ballot for the {lottery_date} lottery is submitted by user: {winning_ballot.user.username}")

def close_lottery_and_select_winner(session, closing_time: str):
    """Close the lottery at closing_time and select a random winner"""
    current_time = datetime.now()
    
    if current_time >= closing_time: # TODO, check if it's effectively working
        # Past midnight so we close the lottery and declare a winner
        close_open_lotteries(session)
        yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        # Check the winner from yesterday
        check_winning_ballot_by_date(session, yesterday)
        # # Reschedule the function for the next day
        # schedule_next_run(session, closing_time)

# SCHEDULING for midnight closing of lottery 
#@repeat(every().day.at("00:00"))
@repeat(every(5).seconds)
def do_at_midnight():
    """Schedule the next run of the function at midnight"""
    next_run_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    close_lottery_and_select_winner(session, next_run_time)
    create_lottery(session, "Loto" + str(next_run_time)[0:10], next_run_time)
    print(f"Next run scheduled for: {next_run_time}")



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
    print(f"Ballot from {user.username} submitted successfully to lottery from {lottery.closing_date}.")


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

def test_db():
    # Example usage
    register_user("HarryPotter", "pass123")
    register_user("HermioneGranger", "pass456")
    create_lottery("LaLoto", datetime(2023,1, 22))
    submit_ballot(1, 1)
    submit_ballot(2, 1)
    submit_ballot(1, 1)


