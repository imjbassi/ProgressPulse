# ProgressPulse - Fitness Tracking Application

Track your fitness journey with ProgressPulse, a GUI-based fitness tracking application built using Python and MySQL.

## Introduction

ProgressPulse is a fitness tracking application that allows users to log their workouts, nutrition intake, goals, and more. The application is built with a user-friendly graphical interface using the Tkinter library and stores data in a MySQL database.

## Features

- Log and manage workouts with details like date, workout type, and duration.
- Keep track of nutrition intake with meal details and calorie counts.
- Set fitness goals with target values and dates for various types of achievements.
- User-friendly GUI interface for easy data entry and visualization.

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/ProgressPulse.git


2. Install required dependencies:

pip install -r requirements.txt


3. Update database configuration in the code (`connect` function) with your MySQL credentials.

## Usage

1. Run the application:

python progress_pulse_app.py


2. Input user data and use the GUI interface to log workouts, nutrition, and goals.

3. Make sure you have a MySQL server running and properly configured.

## Screenshots

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

## Database Schema

- Users (user_id, username, email, password)
- Workouts (workout_id, user_id, date, workout_type, duration)
- Nutrition (nutrition_id, user_id, date, meal_type, calories)
- Goals (goal_id, user_id, goal_type, target_value, target_date)

## Known Issues

- List any known issues or limitations in the application here.

## Contributions

Contributions are welcome! If you have ideas, bug reports, or feature requests, feel free to open an issue or submit a pull request.

## Disclaimer

ProgressPulse is a personal project created for learning purposes. Use it responsibly and make sure to follow best practices for fitness and health.

## License

This project is licensed under the [MIT License](LICENSE).

