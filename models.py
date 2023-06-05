from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Lottery(Base):
    __tablename__ = 'lotteries'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    closing_date = Column(DateTime)
    winning_ballot_id = Column(Integer, ForeignKey('ballots.id'), nullable=True)

class Ballot(Base):
    __tablename__ = 'ballots'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    lottery_id = Column(Integer, ForeignKey('lotteries.id'))
    user = relationship('User', foreign_keys=[user_id])
    lottery = relationship('Lottery', foreign_keys=[lottery_id])
