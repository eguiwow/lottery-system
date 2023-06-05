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

1. Uncomment ```populate_db()``` function in ```main.py```.
2. Start the lottery system:
```
python main.py
```
3. The system will wait until midnight (00:00) to close the current lottery and select a random winner.
