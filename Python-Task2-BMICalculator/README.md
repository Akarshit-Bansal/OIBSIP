# Advanced BMI Calculator

A desktop-based BMI Calculator built with Python Tkinter, SQLite, and Matplotlib.

This project was developed as part of the Oasis Infobyte Python Programming Internship.

## Features

- User-friendly graphical interface using Tkinter
- BMI calculation using weight and height
- BMI category classification
- Color-coded BMI results
- Named user support
- Multiple users can maintain separate BMI histories
- Persistent BMI records using SQLite
- BMI history table
- BMI trend visualization using Matplotlib
- Input validation and error handling
- Database error handling
- Clear/reset functionality

## BMI Categories

| BMI Range | Category |
|-----------|----------|
| Below 18.5 | Underweight |
| 18.5 - 24.9 | Normal |
| 25 - 29.9 | Overweight |
| 30 and above | Obese |

## BMI Formula

BMI is calculated using:

BMI = Weight (kg) / Height² (m)

The application accepts height in centimeters and internally converts it to meters.

## Technology Stack

- Python 3.11
- Tkinter
- SQLite3
- Matplotlib

## Project Structure

```text
Python-Task2-BMICalculator/
│
├── src/
│   ├── __init__.py
│   ├── bmi.py
│   ├── database.py
│   └── main.py
│
├── data/
│   └── bmi_records.db
│
├── screenshots/
│
├── README.md
├── requirements.txt
└── .gitignore