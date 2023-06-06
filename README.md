# Simple Lottery System

This is a simple lottery system written in Python that allows users to participate in a lottery and have a chance to win prizes. Every day a lottery event is held. The users can submit as many ballots as they want to that lottery. Every day at midnight the lottery closes and the system randomly selects a winner from the pool of participants. A new lottery is created for the coming day.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Console Interaction](#console-interaction)
- [Structure](#structure)

## Features

- Participants can get lottery tickets.
- Random selection of the winner at midnight*.
- Display of winners.
- \**If the -m flag is set, the lottery event happens every minute.*

## Prerequisites

Before installing and using this lottery system, make sure you have the following prerequisites:

- Python 3.x
- pip

## Installation

To install the lottery system, follow these steps:

1. Clone the repository:
```
git clone https://github.com/your-username/lottery-system.git
```
2. Navigate to the project directory:
```
cd lottery-system
```
3. Install the required dependencies (use your preferred virtualenv if needed):
```
pip install -r requirements.txt
```

## Usage

1. Start the lottery system and populate the database by running ```main.py``` with ```-p```.
```
python main.py -p
```
2. Run the script without the ```-p``` flag if you don't need to populate the database.
```
python main.py
```
3. Run the script with ```-m``` to launch the lottery event every minute.
```
python main.py -m
```
4. The system will wait until midnight (00:00) to close the current lottery and select a random winner unless the ```-m``` flag is set. 
5. Consult the database file (```lottery.db```) with a .db analysing tool such as DB Browser.

## Console Interaction

The lottery system provides the following options for console interaction:

1. Register in the system
2. Log into the system
3. Submit a ballot for a particular date
4. Submit a ballot for the last open lottery
5. Check the ballot of a particular date  
q. Exit

### Option 1 - Register in the system

This option allows users to register in the lottery system. Users can provide their details such as name, and password to create an account.

### Option 2 - Log into the system

Users who have already registered can use this option to log in to the lottery system. They will be prompted to enter their credentials, such as username and password, for authentication.

### Option 3 - Submit a ballot for a particular date

Users can choose this option to submit a ballot for a specific date. They will be prompted to enter their chosen date.

### Option 4 - Submit a ballot for the last open lottery

If there is an open lottery for participation, users can select this option to submit a ballot for the latest available lottery. This option saves users from manually specifying the date of the lottery draw.

### Option 5 - Check the ballot of a particular date

By selecting this option, users can check the results of the lottery draw for a specific date. They will be prompted to enter the date for which they want to view the ballot results.

### Option q - Exit

Users can choose this option to exit or quit the lottery system console interface.


## Structure

This system is using a tailored backend system in Python with an ORM mapper (SQLAlchemy) that uses a database schema defined in ```models.py```.

The repository contains the following files and directories:

-   `main.py`: runs the main program and populates the database.
-   `__init__.py`: initializes the SQLAlchemy Session to interact with the database.
-   `functions.py`: all the necessary functions to interact with the database and the system.
-   `models.py`: ORM-like database schema.
-   `console_interaction.py`: provides the console interaction logic.
-   `README.md`: this file.

Feel free to contact me for further requests and to adapt this README file to suit your project's specific needs.
