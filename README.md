# Simple Lottery System

This is a simple lottery system written in Python that allows users to participate in a lottery and have a chance to win prizes. Every day a lottery event is held. The users can submit as many ballots as they want to that lottery. Every day at midnight the lottery closes and the system randomly selects a winner from the pool of participants. A new lottery is created for the coming day.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Participants can buy lottery tickets.
- Random selection of the winner.
- Display of winners.

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
2. Run the script without the ```-p``` parameter if you don't need to populate the database.
```
python main.py
```
3. The system will wait until midnight (00:00) to close the current lottery and select a random winner.
4. Consult the database file (```lottery.db```) with a .db analysing tool such as DB Browser.

## Structure

This system is using a tailored backend system in Python with an ORM mapper (SQLAlchemy) that uses a database schema defined in ```models.py```.

The repository contains the following files and directories:

-   `main.py`: runs the main program and populates the database.
-   `__init__.py`: initializes the SQLAlchemy Session to interact with the database.
-   `functions.py`: all the necessary functions to interact with the database and the system.
-   `models.py`: ORM-like database schema.
-   `README.md`: this file.

Feel free to contact me for further requests and to adapt this README file to suit your project's specific needs.
