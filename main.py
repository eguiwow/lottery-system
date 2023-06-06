from datetime import datetime, timedelta
import time
from schedule import run_pending, every
from functions import schedule_midnight, schedule_minute, do_every_minute, do_at_midnight, run_scheduled_process, register_user, create_lottery, populate_db
from console_interaction import interact_user
from __init__ import session
import argparse
import threading
import signal
import sys

origin_date = datetime.strptime("2023-05-18", "%Y-%m-%d")

def main():
    
    # Populate database with -p flag
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

    # Signal handler for termination of program
    def handle_termination(signal, frame):
        print("Received termination signal. Terminating the program.")
        terminate_flag.set()  # Set the termination flag
        sys.exit(0)

    # Register the termination signal handler
    signal.signal(signal.SIGINT, handle_termination)
    signal.signal(signal.SIGTERM, handle_termination)
    
    # THREADING
    terminate_flag = threading.Event()
    # Create and start the threads
    interact_thread = threading.Thread(target=interact_user, args=(session, terminate_flag, args.m,))
    scheduled_process_thread = threading.Thread(target=run_scheduled_process, args=(terminate_flag,))

    interact_thread.start()
    scheduled_process_thread.start()

    # Wait for the threads to complete
    interact_thread.join()
    scheduled_process_thread.join()


if __name__== "__main__":
    main()