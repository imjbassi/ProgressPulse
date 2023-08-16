CREATE DATABASE ProgressPulseDB;

USE ProgressPulseDB;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Workouts (
    workout_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    workout_type VARCHAR(255),
    duration INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Nutrition (
    nutrition_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    meal_type VARCHAR(255),
    calories INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Goals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    goal_type VARCHAR(255),
    target_value INT,
    target_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);