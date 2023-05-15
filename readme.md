# Personal Schedule Planner

A Python script that generates a personalized schedule for daily tasks, weekly tasks, and rotating activities such as side projects, books, and courses. The generated schedule is in the form of an iCalendar file (.ics) that can be imported into many popular calendar applications.

## Features

- Customizable daily and weekly tasks
- Rotating side projects, books, and courses based on user-defined durations
- Personalized task names using placeholders

## Requirements

- Python 3.0 or later


## Installation

1. Clone the repository:

```
git clone https://github.com/conceptcodes/stay-woke.git
```

2. Install the required libraries:

```
pip install -r requirements.txt
```

## Usage

1. Create a `config.yml` file in the root directory of the repository. 

```
cp sample.yaml config.yml
```

2. Run the script:

```
python main.py
```

3. The script will generate a file named `personal_schedule.ics` in the same directory.

4. Import the `personal_schedule.ics` file into your preferred calendar application (e.g., Google Calendar, Microsoft Outlook, Apple Calendar).

## Roadmap

- Add proper unit tests
- Implement a user-friendly command-line interface for customizing the configuration
- Create a web application to allow users to create and modify schedules through a graphical interface




