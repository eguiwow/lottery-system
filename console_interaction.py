import datetime
import os
from functions import register_user, login_user, submit_ballot_date, check_winning_ballot_by_date, get_last_open_lottery

registered = False  # Flag to track registration status
registered_username = "" 

def register(session):
    clear_screen()
    print("Registration form")
    global registered
    global registered_username

    username = input("Enter username: ")
    password = input("Enter password: ")

    if isinstance(username, str) and isinstance(password, str):
        if (register_user(session, username, password)):
            registered = True
            registered_username = username
            print("Registration successful!")
        else:
            print("This username is already in use.")
    else:
        print("Invalid username or password.")

def login(session):
    clear_screen()
    print("Login form")
    global registered
    global registered_username

    username = input("Enter username: ")
    password = input("Enter password: ")

    if isinstance(username, str) and isinstance(password, str):
        if (login_user(session, username, password)):
            registered = True
            registered_username = username
            print("Login successful!")
        else:
            print("Invalid username or password.")
    else:
        print("Invalid username or password.")

def submit_ballot(session):
    clear_screen()    
    if not registered:
        print("You must be registered to submit a ballot.")
        return
    
    date_str = input("Enter the date for the ballot (YYYY-MM-DD): ")
    time_str = input("Enter the time for the ballot (HH:MM): ")

    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.datetime.strptime(time_str, "%H:%M").time()
        ballot_datetime = datetime.datetime.combine(date, time)
        print(f"Submitting ballot for {ballot_datetime}")
        submit_ballot_date(session, registered_username, ballot_datetime)
    except ValueError:
        print("Invalid date or time format. Please try again.")

def submit_ballot_open(session):
    clear_screen()
    if not registered:
        print("You must be registered to submit a ballot.")
        return
    try:
        lottery_date = get_last_open_lottery(session)
        print(f"Submitting ballot for {lottery_date}")
        submit_ballot_date(session, registered_username, lottery_date)
    except ValueError:
        print("Invalid date or time format. Please try again.")


def check_ballot(session):
    clear_screen()
    date_str = input("Enter the date to check the ballot (YYYY-MM-DD): ")
    time_str = input("Enter the time to check the ballot (HH:MM): ")

    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.datetime.strptime(time_str, "%H:%M").time()
        ballot_datetime = datetime.datetime.combine(date, time)
        print(f"Checking ballot for {ballot_datetime}", flush=True)
        check_winning_ballot_by_date(session, ballot_datetime)
    except ValueError:
        print("Invalid date or time format. Please try again.")

def clear_screen():
    # Check the operating system and execute the appropriate command
    if os.name == "nt":
        os.system("cls")  # For Windows
    else:
        os.system("clear")  # For Linux and macOS

def interact_user(session, terminate_flag):
    while not terminate_flag.is_set():
        print("\nOptions:")
        print("1 - Register in the system")
        print("2 - Login into the system")        
        print("3 - Submit a ballot for a particular date")
        print("4 - Submit a ballot for the last open lottery")        
        print("5 - Check the ballot of a particular date")
        print("q - Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register(session)
        elif choice == "2":
            login(session)
        elif choice == "3":
            submit_ballot(session)
        elif choice == "4":
            submit_ballot_open(session)
        elif choice == "5":
            check_ballot(session)
        elif choice == "q":
            terminate_flag.set()
        else:
            print("Invalid choice. Please try again.")
            clear_screen()
