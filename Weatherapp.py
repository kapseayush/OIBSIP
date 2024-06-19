import tkinter as tk
from tkinter import messagebox
import requests
from geopy.geocoders import Nominatim


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x400")

        self.api_key = "YOUR_API_KEY"

        self.create_widgets()

    def create_widgets(self):
        # Entry for manual location input
        self.location_entry = tk.Entry(self.root, width=30)
        self.location_entry.grid(row=0, column=0, padx=10, pady=10)

        # Button to fetch weather by location
        self.fetch_weather_button = tk.Button(self.root, text="Get Weather", command=self.fetch_weather)
        self.fetch_weather_button.grid(row=0, column=1, padx=10, pady=10)

        # Button to fetch weather by GPS
        self.gps_button = tk.Button(self.root, text="Use GPS", command=self.fetch_weather_by_gps)
        self.gps_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Labels to display weather info
        self.weather_info = tk.Label(self.root, text="", justify="left")
        self.weather_info.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def fetch_weather(self):
        location = self.location_entry.get()
        if not location:
            messagebox.showwarning("Input Error", "Please enter a location.")
            return
        self.get_weather_data(location)

    def fetch_weather_by_gps(self):
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode("YOUR_ADDRESS_HERE")
        if location:
            self.get_weather_data(f"{location.latitude},{location.longitude}")
        else:
            messagebox.showerror("GPS Error", "Could not determine GPS location.")

    def get_weather_data(self, location):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.display_weather(data)
        else:
            messagebox.showerror("API Error", "Could not fetch weather data.")

    def display_weather(self, data):
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        weather_info = (f"Weather: {weather_desc}\n"
                        f"Temperature: {temp}°C\n"
                        f"Humidity: {humidity}%\n"
                        f"Wind Speed: {wind_speed} m/s")
        self.weather_info.config(text=weather_info)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
