import io
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import requests
from PIL import Image, ImageTk

from src.weather_api import (
    get_current_weather,
    get_forecast,
    WeatherAPIError,
)

from src.weather_utils import (
    parse_forecast_entries,
    get_next_hours,
    get_daily_forecast,
    format_temperature,
    format_wind_speed,
    icon_url,
)


class WeatherApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Weather Dashboard")
        self.root.geometry("1050x780")
        self.root.minsize(900, 700)

        # Application state
        self.unit = "C"
        self.current_weather = None
        self.forecast_entries = []

        self.setup_style()
        self.create_variables()
        self.create_widgets()

    # =========================================================
    # VARIABLES
    # =========================================================

    def create_variables(self):
        self.city_var = tk.StringVar()

        self.status_var = tk.StringVar(
            value="Enter a city and click Get Weather."
        )

        self.temperature_var = tk.StringVar(
            value="-- °C"
        )

        self.condition_var = tk.StringVar(
            value="--"
        )

        self.description_var = tk.StringVar(
            value="--"
        )

        self.humidity_var = tk.StringVar(
            value="Humidity: --"
        )

        self.wind_var = tk.StringVar(
            value="Wind: --"
        )

    # =========================================================
    # STYLE
    # =========================================================

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold"),
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 10),
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 14, "bold"),
        )

        style.configure(
            "Temperature.TLabel",
            font=("Segoe UI", 34, "bold"),
        )

        style.configure(
            "Condition.TLabel",
            font=("Segoe UI", 15, "bold"),
        )

        style.configure(
            "WeatherInfo.TLabel",
            font=("Segoe UI", 11),
        )

        style.configure(
            "Forecast.TLabel",
            font=("Segoe UI", 9),
        )

        style.configure(
            "GetWeather.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )

    # =========================================================
    # CREATE GUI
    # =========================================================

    def create_widgets(self):
        main = ttk.Frame(
            self.root,
            padding=20,
        )

        main.pack(
            fill="both",
            expand=True,
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        ttk.Label(
            main,
            text="Weather Dashboard",
            style="Title.TLabel",
        ).pack()

        ttk.Label(
            main,
            text="Real-time weather and forecast information",
            style="Subtitle.TLabel",
        ).pack(
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # SEARCH AREA
        # -----------------------------------------------------

        search_frame = ttk.Frame(main)

        search_frame.pack(
            fill="x",
            pady=(0, 10),
        )

        ttk.Label(
            search_frame,
            text="City:",
            font=("Segoe UI", 11, "bold"),
        ).pack(
            side="left",
            padx=(0, 8),
        )

        self.city_entry = ttk.Entry(
            search_frame,
            textvariable=self.city_var,
            font=("Segoe UI", 11),
        )

        self.city_entry.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self.city_entry.bind(
            "<Return>",
            lambda event: self.get_weather(),
        )

        self.get_weather_button = ttk.Button(
            search_frame,
            text="Get Weather",
            command=self.get_weather,
            style="GetWeather.TButton",
        )

        self.get_weather_button.pack(
            side="left",
            padx=8,
        )

        ttk.Button(
            search_frame,
            text="Celsius",
            command=lambda: self.set_unit("C"),
        ).pack(
            side="left",
            padx=2,
        )

        ttk.Button(
            search_frame,
            text="Fahrenheit",
            command=lambda: self.set_unit("F"),
        ).pack(
            side="left",
            padx=2,
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_label = ttk.Label(
            main,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
        )

        self.status_label.pack(
            fill="x",
            pady=(0, 10),
        )

        # -----------------------------------------------------
        # CURRENT WEATHER
        # -----------------------------------------------------

        current_frame = ttk.LabelFrame(
            main,
            text="Current Weather",
            padding=15,
        )

        current_frame.pack(
            fill="x",
            pady=5,
        )

        current_content = ttk.Frame(
            current_frame
        )

        current_content.pack(
            fill="x"
        )

        # Current icon
        self.current_icon_label = ttk.Label(
            current_content,
            text="☀",
            font=("Segoe UI", 50),
        )

        self.current_icon_label.pack(
            side="left",
            padx=(10, 25),
        )

        # Temperature / condition
        temperature_content = ttk.Frame(
            current_content
        )

        temperature_content.pack(
            side="left",
            fill="x",
            expand=True,
        )

        ttk.Label(
            temperature_content,
            textvariable=self.temperature_var,
            style="Temperature.TLabel",
        ).pack(
            anchor="w"
        )

        ttk.Label(
            temperature_content,
            textvariable=self.condition_var,
            style="Condition.TLabel",
        ).pack(
            anchor="w"
        )

        ttk.Label(
            temperature_content,
            textvariable=self.description_var,
        ).pack(
            anchor="w"
        )

        # Humidity / wind
        info_content = ttk.Frame(
            current_content
        )

        info_content.pack(
            side="right",
            padx=20,
        )

        ttk.Label(
            info_content,
            textvariable=self.humidity_var,
            style="WeatherInfo.TLabel",
        ).pack(
            anchor="w",
            pady=3,
        )

        ttk.Label(
            info_content,
            textvariable=self.wind_var,
            style="WeatherInfo.TLabel",
        ).pack(
            anchor="w",
            pady=3,
        )

        # -----------------------------------------------------
        # HOURLY FORECAST
        # -----------------------------------------------------

        ttk.Label(
            main,
            text="Next 6 Hours",
            style="Section.TLabel",
        ).pack(
            anchor="w",
            pady=(15, 5),
        )

        self.hourly_container = ttk.Frame(main)

        self.hourly_container.pack(
            fill="x"
        )

        # -----------------------------------------------------
        # DAILY FORECAST
        # -----------------------------------------------------

        ttk.Label(
            main,
            text="Next 5 Days",
            style="Section.TLabel",
        ).pack(
            anchor="w",
            pady=(15, 5),
        )

        self.daily_container = ttk.Frame(main)

        self.daily_container.pack(
            fill="both",
            expand=True,
        )

        # Initial placeholders
        self.show_hourly_placeholders()
        self.show_daily_placeholders()

    # =========================================================
    # GET WEATHER
    # =========================================================

    def get_weather(self):
        city = self.city_var.get().strip()

        if not city:
            self.show_error(
                "Please enter a city name."
            )
            return

        self.set_loading_state(True)

        self.status_var.set(
            f"Loading weather for {city}..."
        )

        self.get_weather_button.configure(
            state="disabled"
        )

        worker = threading.Thread(
            target=self.fetch_weather,
            args=(city,),
            daemon=True,
        )

        worker.start()

    # =========================================================
    # FETCH WEATHER
    # =========================================================

    def fetch_weather(self, city):
        """
        Fetch current weather first.

        Forecast is fetched separately so that a forecast
        problem does not prevent current weather from being
        displayed.
        """

        try:

            # -------------------------------------------------
            # CURRENT WEATHER
            # -------------------------------------------------

            current = get_current_weather(city)

            self.root.after(
                0,
                lambda: self.update_current_weather_result(
                    current
                ),
            )

            # -------------------------------------------------
            # FORECAST
            # -------------------------------------------------

            try:

                forecast_data = get_forecast(city)

                entries = parse_forecast_entries(
                    forecast_data
                )

                self.root.after(
                    0,
                    lambda: self.update_forecast_result(
                        entries
                    ),
                )

            except WeatherAPIError as error:

                self.root.after(
                    0,
                    lambda: self.show_forecast_error(
                        str(error)
                    ),
                )

            except Exception as error:

                self.root.after(
                    0,
                    lambda: self.show_forecast_error(
                        f"Forecast error: {error}"
                    ),
                )

        except ValueError as error:

            self.root.after(
                0,
                lambda: self.show_error(
                    str(error)
                ),
            )

        except WeatherAPIError as error:

            self.root.after(
                0,
                lambda: self.show_error(
                    str(error)
                ),
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: self.show_error(
                    f"Unexpected error: {error}"
                ),
            )

    # =========================================================
    # CURRENT WEATHER RESULT
    # =========================================================

    def update_current_weather_result(
        self,
        current,
    ):
        """
        Update the GUI immediately after current weather
        has been successfully received.
        """

        self.current_weather = current

        location = current.get(
            "city",
            "Unknown",
        )

        country = current.get(
            "country",
            "",
        )

        if country:
            location = f"{location}, {country}"

        self.status_var.set(
            f"Current weather loaded — {location}"
        )

        self.update_current_weather()

        self.set_loading_state(False)

    # =========================================================
    # FORECAST RESULT
    # =========================================================

    def update_forecast_result(
        self,
        entries,
    ):
        """
        Update hourly and daily forecast sections.
        """

        self.forecast_entries = entries

        self.update_hourly_forecast()

        self.update_daily_forecast()

        if self.current_weather:

            location = self.current_weather.get(
                "city",
                "Unknown",
            )

            country = self.current_weather.get(
                "country",
                "",
            )

            if country:
                location = f"{location}, {country}"

            self.status_var.set(
                f"Weather and forecast updated — {location}"
            )

    # =========================================================
    # CURRENT WEATHER DISPLAY
    # =========================================================

    def update_current_weather(self):

        if not self.current_weather:
            return

        weather = self.current_weather

        temperature = weather.get(
            "temperature_c"
        )

        if temperature is not None:

            self.temperature_var.set(
                format_temperature(
                    temperature,
                    self.unit,
                )
            )

        self.condition_var.set(
            weather.get(
                "condition",
                "--",
            )
        )

        self.description_var.set(
            weather.get(
                "description",
                "--",
            )
        )

        self.humidity_var.set(
            f"Humidity: "
            f"{weather.get('humidity', '--')}%"
        )

        wind_speed = weather.get(
            "wind_speed",
            0,
        )

        self.wind_var.set(
            f"Wind: "
            f"{format_wind_speed(wind_speed)}"
        )

        icon_code = weather.get(
            "icon"
        )

        self.load_weather_icon(
            icon_code,
            self.current_icon_label,
            size=(90, 90),
        )

    # =========================================================
    # UNIT TOGGLE
    # =========================================================

    def set_unit(self, unit):

        self.unit = unit

        if self.current_weather:

            self.update_current_weather()

            self.update_hourly_forecast()

            self.update_daily_forecast()

            if unit == "C":
                unit_name = "Celsius"
            else:
                unit_name = "Fahrenheit"

            self.status_var.set(
                f"Temperature unit changed to "
                f"{unit_name}."
            )

    # =========================================================
    # HOURLY FORECAST
    # =========================================================

    def update_hourly_forecast(self):

        self.clear_container(
            self.hourly_container
        )

        entries = get_next_hours(
            self.forecast_entries,
            6,
        )

        if not entries:

            ttk.Label(
                self.hourly_container,
                text="Hourly forecast unavailable.",
            ).pack()

            return

        for entry in entries:

            card = ttk.Frame(
                self.hourly_container,
                relief="ridge",
                borderwidth=1,
                padding=8,
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=3,
            )

            date_time = entry.get(
                "datetime"
            )

            if date_time:

                time_text = date_time.strftime(
                    "%I %p"
                ).lstrip("0")

            else:

                time_text = "--"

            ttk.Label(
                card,
                text=time_text,
                font=("Segoe UI", 9, "bold"),
            ).pack()

            icon_label = ttk.Label(
                card,
                text="☁",
                font=("Segoe UI", 20),
            )

            icon_label.pack(
                pady=4
            )

            self.load_weather_icon(
                entry.get("icon"),
                icon_label,
                size=(50, 50),
            )

            temperature = entry.get(
                "temperature_c"
            )

            if temperature is not None:

                temperature_text = format_temperature(
                    temperature,
                    self.unit,
                )

            else:

                temperature_text = "--"

            ttk.Label(
                card,
                text=temperature_text,
                font=("Segoe UI", 10, "bold"),
            ).pack()

            ttk.Label(
                card,
                text=entry.get(
                    "condition",
                    "--",
                ),
                style="Forecast.TLabel",
            ).pack()

    # =========================================================
    # DAILY FORECAST
    # =========================================================

    def update_daily_forecast(self):

        self.clear_container(
            self.daily_container
        )

        daily = get_daily_forecast(
            self.forecast_entries,
            5,
        )

        if not daily:

            ttk.Label(
                self.daily_container,
                text="Daily forecast unavailable.",
            ).pack()

            return

        for entry in daily:

            card = ttk.Frame(
                self.daily_container,
                relief="ridge",
                borderwidth=1,
                padding=10,
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=3,
            )

            date_value = entry.get(
                "date"
            )

            if date_value:

                day_text = date_value.strftime(
                    "%a, %d %b"
                )

            else:

                day_text = "--"

            ttk.Label(
                card,
                text=day_text,
                font=("Segoe UI", 10, "bold"),
            ).pack()

            icon_label = ttk.Label(
                card,
                text="☁",
                font=("Segoe UI", 24),
            )

            icon_label.pack(
                pady=5
            )

            self.load_weather_icon(
                entry.get("icon"),
                icon_label,
                size=(60, 60),
            )

            ttk.Label(
                card,
                text=entry.get(
                    "condition",
                    "--",
                ),
                font=("Segoe UI", 9, "bold"),
            ).pack()

            max_temperature = entry.get(
                "max_temperature_c"
            )

            min_temperature = entry.get(
                "min_temperature_c"
            )

            if max_temperature is not None:

                high_text = format_temperature(
                    max_temperature,
                    self.unit,
                )

            else:

                high_text = "--"

            if min_temperature is not None:

                low_text = format_temperature(
                    min_temperature,
                    self.unit,
                )

            else:

                low_text = "--"

            ttk.Label(
                card,
                text=f"High: {high_text}",
            ).pack()

            ttk.Label(
                card,
                text=f"Low: {low_text}",
            ).pack()

    # =========================================================
    # WEATHER ICONS
    # =========================================================

    def load_weather_icon(
        self,
        icon_code,
        label,
        size=(70, 70),
    ):
        """
        Download the icon in a background thread.

        ImageTk.PhotoImage is created on the Tkinter main
        thread, which avoids Tkinter thread-safety problems.
        """

        url = icon_url(icon_code)

        if not url:
            return

        def download_icon():

            try:

                response = requests.get(
                    url,
                    timeout=10,
                )

                response.raise_for_status()

                image_data = response.content

                self.root.after(
                    0,
                    lambda: self.apply_weather_icon(
                        label,
                        image_data,
                        size,
                    ),
                )

            except Exception:
                # Keep the text placeholder if the icon
                # cannot be downloaded.
                pass

        threading.Thread(
            target=download_icon,
            daemon=True,
        ).start()

    def apply_weather_icon(
        self,
        label,
        image_data,
        size,
    ):
        """
        Create and apply the Tkinter image on the
        main GUI thread.
        """

        try:

            image = Image.open(
                io.BytesIO(image_data)
            )

            image = image.convert(
                "RGBA"
            )

            image = image.resize(
                size,
                Image.Resampling.LANCZOS,
            )

            photo = ImageTk.PhotoImage(
                image
            )

            label.configure(
                image=photo,
                text="",
            )

            # Keep reference alive.
            label.image = photo

        except Exception:
            pass

    # =========================================================
    # LOADING STATE
    # =========================================================

    def set_loading_state(
        self,
        loading,
    ):

        if loading:

            self.get_weather_button.configure(
                state="disabled"
            )

            self.status_var.set(
                "Fetching weather data..."
            )

        else:

            self.get_weather_button.configure(
                state="normal"
            )

    # =========================================================
    # ERRORS
    # =========================================================

    def show_error(
        self,
        message,
    ):

        self.set_loading_state(False)

        self.status_var.set(
            f"Error: {message}"
        )

        messagebox.showerror(
            "Weather Error",
            message,
            parent=self.root,
        )

    def show_forecast_error(
        self,
        message,
    ):
        """
        Current weather remains visible even if forecast
        retrieval fails.
        """

        self.set_loading_state(False)

        self.status_var.set(
            "Current weather loaded. "
            f"Forecast unavailable: {message}"
        )

    # =========================================================
    # PLACEHOLDERS
    # =========================================================

    def show_hourly_placeholders(self):

        for _ in range(6):

            card = ttk.Frame(
                self.hourly_container,
                relief="ridge",
                borderwidth=1,
                padding=8,
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=3,
            )

            ttk.Label(
                card,
                text="--",
            ).pack()

            ttk.Label(
                card,
                text="☁",
                font=("Segoe UI", 24),
            ).pack(
                pady=5
            )

            ttk.Label(
                card,
                text="-- °C",
            ).pack()

    def show_daily_placeholders(self):

        for _ in range(5):

            card = ttk.Frame(
                self.daily_container,
                relief="ridge",
                borderwidth=1,
                padding=10,
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=3,
            )

            ttk.Label(
                card,
                text="--",
            ).pack()

            ttk.Label(
                card,
                text="☁",
                font=("Segoe UI", 28),
            ).pack(
                pady=5
            )

            ttk.Label(
                card,
                text="--",
            ).pack()

    # =========================================================
    # UTILITY
    # =========================================================

    @staticmethod
    def clear_container(
        container
    ):

        for widget in container.winfo_children():
            widget.destroy()


# =============================================================
# APPLICATION START
# =============================================================

def main():

    root = tk.Tk()

    WeatherApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()