# OIBSIP Task 4 - Advanced Weather Dashboard

## Overview

This project is an Advanced Weather Dashboard developed in Python as part of the Oasis Infobyte Python Programming Internship.

The application retrieves real-time weather information and forecasts from the OpenWeatherMap API and displays the information through a Tkinter graphical interface.

## Features

### Current Weather

- Search weather by city name
- Current temperature in Celsius
- Current temperature in Fahrenheit
- Feels-like weather data available through the API layer
- Humidity percentage
- Wind speed
- Weather condition
- Weather description
- OpenWeatherMap weather icon

### Forecast

- Next 6 forecast periods displayed in the hourly forecast section
- Next 5 days displayed in the daily forecast section
- Daily high and low temperatures
- Weather condition and icons

### Unit Conversion

The application supports:

- Celsius
- Fahrenheit

Users can switch between the two units without requesting the weather again.

### Error Handling

The application handles:

- Empty city input
- City not found
- Invalid API key
- API/network errors
- Request timeout
- API rate-limit errors
- Invalid API responses

Errors are displayed inside the GUI.

### Responsive Interface

Weather API requests run in a background thread so that the Tkinter interface remains responsive while network requests are being processed.

## Technology Stack

- Python 3
- Tkinter
- Requests
- Pillow
- python-dotenv
- OpenWeatherMap API

## Project Structure

```text
Python-Task4-WeatherApp/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── weather_api.py
│   └── weather_utils.py
│
├── assets/
│   └── icons/
│
├── screenshots/
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt