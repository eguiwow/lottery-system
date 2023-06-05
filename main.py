from datetime import datetime, timedelta
import time
from schedule import run_pending
from functions import do_at_midnight, register_user, create_lottery, populate_db
from __init__ import session
import argparse

origin_date = datetime.strptime("2023-05-18", "%Y-%m-%d")

def main():
 
    # Populate database with -p flag
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true', help='Populate the database')
    args = parser.parse_args()

    if args.p:
        populate_db(session, origin_date)

    # Testing some functions...
    # check_winning_ballot_by_date(session, origin_date)
    # today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # create_lottery(session, "Loto" + str(today)[0:10], today)

    # Start the initial scheduling
    do_at_midnight()

    while True:
        # schedule for every day at midnight
        run_pending()
        time.sleep(1)

if __name__== "__main__":
    main()
    
    # just testin'
