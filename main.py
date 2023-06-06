from datetime import datetime, timedelta
import time
from schedule import run_pending, every
from functions import schedule_midnight, schedule_minute, do_every_minute, do_at_midnight, register_user, create_lottery, populate_db
from __init__ import session
import argparse

origin_date = datetime.strptime("2023-05-18", "%Y-%m-%d")

def main():
 
    # Populate database with -p parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true', help='Populate the database')
    parser.add_argument('-m', action='store_true', help='Minute lottery mode')
    args = parser.parse_args()
    
    if args.p:
        populate_db(session, origin_date)

    if args.m:
        # Do once to prove how it works
        do_every_minute()
        # Start the initial scheduling every minute
        schedule_minute()
    else:
        # Do once to prove how it works
        do_at_midnight()
        # Start the initial scheduling at midnight        
        schedule_midnight()
        
    # Testing some functions...
    # -------------------------
    # check_winning_ballot_by_date(session, origin_date)
    # today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # create_lottery(session, "Loto" + str(today)[0:10], today)

    while True:
        # schedule for every day at midnight
        run_pending()
        time.sleep(1)

if __name__== "__main__":
    main()
    