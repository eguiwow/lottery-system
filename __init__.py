from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from datetime import datetime

# Create database connection
engine = create_engine('sqlite:///lottery.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create database tables
Base.metadata.create_all(engine)
