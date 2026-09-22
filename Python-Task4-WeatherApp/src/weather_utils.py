from datetime import datetime


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def format_temperature(celsius, unit="C"):
    """Format a temperature according to the selected unit."""

    if unit.upper() == "F":
        temperature = celsius_to_fahrenheit(celsius)
        return f"{temperature:.1f} °F"

    return f"{celsius:.1f} °C"


def format_wind_speed(speed_mps):
    """Format wind speed in meters per second."""
    return f"{speed_mps:.1f} m/s"


def parse_forecast_entries(data):
    """
    Convert the OpenWeatherMap forecast response into
    simplified forecast records.
    """

    entries = []

    for item in data.get("list", []):
        weather = item.get("weather", [{}])[0]
        main = item.get("main", {})
        wind = item.get("wind", {})

        timestamp = item.get("dt")

        if timestamp:
            date_time = datetime.fromtimestamp(timestamp)
        else:
            date_time = None

        entries.append(
            {
                "datetime": date_time,
                "temperature_c": main.get("temp"),
                "feels_like_c": main.get("feels_like"),
                "humidity": main.get("humidity"),
                "condition": weather.get("main", ""),
                "description": weather.get(
                    "description",
                    "",
                ).title(),
                "icon": weather.get("icon", ""),
                "wind_speed": wind.get("speed", 0),
            }
        )

    return entries


def get_next_hours(entries, hours=6):
    """
    Return forecast entries covering approximately
    the next requested number of hours.
    """

    valid_entries = [
        entry
        for entry in entries
        if entry.get("datetime") is not None
    ]

    return valid_entries[:hours]


def get_daily_forecast(entries, days=5):
    """
    Group 3-hour forecast entries by calendar date and
    return one representative forecast for each day.

    The entry closest to midday is used as the representative
    daily forecast.
    """

    grouped = {}

    for entry in entries:
        date_time = entry.get("datetime")

        if date_time is None:
            continue

        date_key = date_time.date()

        grouped.setdefault(date_key, []).append(entry)

    daily = []

    for date_key, day_entries in sorted(grouped.items()):

        # Prefer an entry around 12:00.
        representative = min(
            day_entries,
            key=lambda item: abs(
                item["datetime"].hour - 12
            ),
        )

        temperatures = [
            item["temperature_c"]
            for item in day_entries
            if item["temperature_c"] is not None
        ]

        min_temperature = (
            min(temperatures)
            if temperatures
            else None
        )

        max_temperature = (
            max(temperatures)
            if temperatures
            else None
        )

        daily.append(
            {
                "date": date_key,
                "datetime": representative["datetime"],
                "temperature_c": representative[
                    "temperature_c"
                ],
                "min_temperature_c": min_temperature,
                "max_temperature_c": max_temperature,
                "condition": representative["condition"],
                "description": representative["description"],
                "icon": representative["icon"],
                "humidity": representative["humidity"],
                "wind_speed": representative["wind_speed"],
            }
        )

        if len(daily) >= days:
            break

    return daily


def icon_url(icon_code):
    """Return the OpenWeatherMap icon URL."""

    if not icon_code:
        return None

    return (
        "https://openweathermap.org/img/wn/"
        f"{icon_code}@2x.png"
    )