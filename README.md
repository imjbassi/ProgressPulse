# ProgressPulse - Fitness Tracking Application

<sup>Made by Jaiveer Bassi for CS360: Database Management Systems </sup>

Track your fitness journey with ProgressPulse, a GUI-based fitness-tracking application built using Python and MySQL.

## Introduction

ProgressPulse is a fitness-tracking application that allows users to log their workouts, nutrition intake, goals, and more. The application is built with a GUI using Tkinter and stores data in a MySQL database.

## Features

- Log and manage workouts with details like date, workout type, and duration.
- Keep track of nutrition intake with meal details and calorie counts.
- Set fitness goals with target values and dates for various types of achievements.
- User-friendly GUI interface for easy data entry and visualization.

<img src="https://raw.githubusercontent.com/imjbassi/ProgressPulse/main/Images/Example.png" width="500">

<img src="https://raw.githubusercontent.com/imjbassi/ProgressPulse/main/Images/GUI1.png" width="200">

## Installation

1. Clone the repository:
`git clone https://github.com/yourusername/ProgressPulse.git`

2. Install required dependencies/libraries:
All database elements were used using MySQL: https://www.mysql.com/downloads/

- Libraries: `pip install -r requirements.txt`
- To get MySQL to work on Mac, which is what I used, you need Homebrew and need to use `brew install mysql-connector-c`, `pip install mysql-python`, and `pip install mysql-connector-python`

3. Update database configuration (`connect` function) with your MySQL info.

## Usage

1. Run the application: `python progresspulse.py`

3. Input user data and use the GUI interface to log workouts, nutrition, and goals.

4. Make sure you have a MySQL server running and properly configured.

## Code
ProgressPulse.py:

<img src="https://raw.githubusercontent.com/imjbassi/ProgressPulse/main/Images/ProgressPulsePY.png" width="800">

Database.sql

<img src="https://raw.githubusercontent.com/imjbassi/ProgressPulse/main/Images/DatabseSQL.png" width="800">

## Python Code

1. **Importing Libraries:**
   The script imports `mysql.connector` for MySQL database interaction and `tkinter` for GUI creation.

2. **Connecting to Database:**
   The code establishes a MySQL connection and cursor for executing queries.

3. **GUI Window Creation:**
   A main window is created with the title "ProgressPulse".

4. **Database Functions:**
   The `add_workout()` function inserts workout data into the `Workouts` table.

5. **GUI Components:**
   Labels, entry fields, and a button are created for user data input.

6. **GUI Layout:**
   Components are arranged vertically for user-friendly input.

7. **Event Loop:**
   The GUI event loop is initiated with `root.mainloop()`.

8. **Database Connection Close:**
   The MySQL connection is closed after GUI interaction.

## Database Schema

- Users (user_id, username, email, password)
- Workouts (workout_id, user_id, date, workout_type, duration)
- Nutrition (nutrition_id, user_id, date, meal_type, calories)
- Goals (goal_id, user_id, goal_type, target_value, target_date)

## Disclaimer

ProgressPulse is a personal project created for a class of mine. I doubt I'll ever update this again.

