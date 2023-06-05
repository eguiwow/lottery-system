from datetime import datetime, timedelta
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
import random as rand
import schedule
import time

# Create database connection
engine = create_engine('sqlite:///lottery.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define the closing time for the lottery (midnight)
closing_time = "00:00"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Lottery(Base):
    __tablename__ = 'lotteries'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    closing_date = Column(DateTime, unique=True)
    winning_ballot_id = Column(Integer, ForeignKey('ballots.id'), nullable=True)

class Ballot(Base):
    __tablename__ = 'ballots'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    lottery_id = Column(Integer, ForeignKey('lotteries.id'))
    user = relationship('User', foreign_keys=[user_id])
    lottery = relationship('Lottery', foreign_keys=[lottery_id])


# Create database tables
Base.metadata.create_all(engine)


def register_user(username: str, password: str):
    """Register a new user"""
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    print("User registered successfully.")


def create_lottery(name: str, closing_date: DateTime):
    """Register a new user"""
    lottery = Lottery(name=name, closing_date=closing_date)
    session.add(lottery)
    session.commit()
    print("Lottery created successfully.")


def submit_ballot(user_id: int, lottery_id: int):
    """Submit a ballot for a specific lottery"""
    lottery = session.query(Lottery).get(lottery_id)

    if lottery.closing_date < datetime.now():
        print("This lottery has already closed.")
        return

    ballot = Ballot(user_id=user_id, lottery_id=lottery_id)
    session.add(ballot)
    session.commit()
    print("Ballot submitted successfully.")

# We get rid of the date constraint to populate the db
def submit_past_ballot(user_id: int, lottery_id: int):
    """Submit a ballot for a specific lottery"""
    lottery = session.query(Lottery).get(lottery_id)
    user = session.query(User).get(user_id)
    ballot = Ballot(user_id=user_id, lottery_id=lottery_id)
    session.add(ballot)
    session.commit()
    print(f"Ballot from {user.username} submitted successfully to lottery from {lottery.name}.")


def close_lotteries():
    """Close open lotteries and select random winners"""
    open_lotteries = session.query(Lottery).filter(Lottery.closing_date <= datetime.now())

    for lottery in open_lotteries.all():
        # random ballot selected as winner
        ballot = session.query(Ballot).filter(Ballot.lottery == lottery).order_by(func.random()).first()
        if ballot:           
            lottery.winning_ballot_id = ballot.id
            session.commit()

        else:
            print(f"No ballots found for lottery with ID: {lottery.id}")

    print("Lotteries closed successfully.")


def check_winning_ballot_by_lottery_id(lottery_id: int):
    """Check the winning ballot for a specific lottery"""
    lottery = session.query(Lottery).get(lottery_id)

    if lottery.winning_ballot_id is None:
        print("No winning ballot found for this lottery.")
    else:
        winning_ballot = session.query(Ballot).get(lottery.winning_ballot_id)
        print(f"The winning ballot for this lottery is submitted by user: {winning_ballot.user.username}")


def check_winning_ballot_by_date(lottery_date: DateTime):
    """Check the winning ballot for a specific lottery"""
    lottery = session.query(Lottery).filter(Lottery.closing_date == lottery_date).first()

    if lottery.winning_ballot_id is None:
        print("No winning ballot found for this lottery.")
    else:
        winning_ballot = session.query(Ballot).get(lottery.winning_ballot_id)
        print(f"The winning ballot for this lottery is submitted by user: {winning_ballot.user.username}")


def populate_db(origin_date: DateTime):
    """Populate the database with test data"""
    # Sample list of names from where to create users
    names = ["Frodo", "Legolas", "Aragorn", "Gandalf", "Gimli", "Pippin", "Merry", "Sam", "Boromir"]
    
    # Get the current date
    current_date = datetime.now().date()
    # Specify the origin date for the lottery
    target_date = datetime(origin_date).date()
    # Calculate the number of days that have passed
    days_passed = (current_date - target_date).days

    # Populate the db with users from list and passwords
    for name in names:
        for i in range(1, 10):
            register_user(name+str(i), "pass"+str(i))
    # Populate the db with a new lottery each day since origin_date
    for i in range(days_passed):
        create_lottery("Loto" + str(i), target_date + timedelta(i))
    
    num_lotteries = session.query(Lottery.id).count()
    num_users = session.query(User.id).count()    
    # Submit ballots from random users to random lotteries
    for i in range(1000):
        submit_past_ballot(rand.randint(1, num_users), rand.randint(1, num_lotteries))


def close_lottery_and_select_winner():
    """Close the lottery and select a random winner"""
    current_time = datetime.now().strftime("%H:%M")
    
    if current_time >= closing_time:
        # Past midnight so we close the lottery and declare a winner
        close_lotteries()        
        # Check the winner
        check_winning_ballot_by_date( datetime.now().date() - timedelta(days=1))
        # Reschedule the function for the next day
        schedule_next_run()

# SCHEDULING for midnight closing of lottery 

def schedule_next_run():
    """Schedule the next run of the function at midnight"""
    next_run_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    schedule.every().day.at(closing_time).do(close_lottery_and_select_winner).tag('lottery_event')
    schedule.every().day.at(closing_time).do(schedule_next_run).tag('schedule_next_run')
    print(f"Next run scheduled for: {next_run_time}")

# Start the initial scheduling
schedule_next_run()

# Keep the script running to allow scheduled tasks to execute
while True:
    time.sleep(1)


# Example usage

# register_user("HarryPotter", "pass123")
# register_user("HermioneGranger", "pass456")
# create_lottery("LaLoto", datetime(2023,1, 22))
# submit_ballot(1, 1)
# submit_ballot(2, 1)
# submit_ballot(1, 1)

origin_date = datetime(2023, 5, 18)

#populate_db(origin_date)

close_lotteries()

check_winning_ballot_by_date(date)
