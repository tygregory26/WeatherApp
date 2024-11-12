import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

# API
apiKey = "c052fbe60abb8f8037eac7b3a1a43a6d"
baseUrl = "http://api.openweathermap.org/data/2.5/"

# Global variables
units = "imperial"

# Function to fetch weather data
def getWeather(location):
    try:
        response = requests.get(f"{baseUrl}weather", params={"q": location, "appid": apiKey, "units": units})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Could not retrieve weather data: {e}")
        return None

# Function to fetch forecast data
def getForecast(location):
    try:
        response = requests.get(f"{baseUrl}forecast", params={"q": location, "appid": apiKey, "units": units})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Could not retrieve forecast data: {e}")
        return None

# Display detailed current weather
def displayDetailedWeather():
    location = locationEntry.get()
    weatherData = getWeather(location)
    
    if weatherData:
        main = weatherData["main"]
        wind = weatherData["wind"]
        sys = weatherData["sys"]
        weatherDesc = weatherData["weather"][0]["description"]
        
        detailedWeather.set(
            f"Location: {weatherData['name']}\n"
            f"Temperature: {main['temp']}° {'F' if units == 'imperial' else 'C'}\n"
            f"Feels Like: {main['feels_like']}°\n"
            f"Humidity: {main['humidity']}%\n"
            f"Pressure: {main['pressure']} hPa\n"
            f"Wind Speed: {wind['speed']} m/s\n"
            f"Sunrise: {convertUnixToTime(sys['sunrise'])}\n"
            f"Sunset: {convertUnixToTime(sys['sunset'])}\n"
            f"Description: {weatherDesc.capitalize()}"
        )

# Convert Unix timestamp to 12-hour format with AM/PM
def convertUnixToTime(unixTimestamp):
    return datetime.fromtimestamp(unixTimestamp).strftime('%I:%M:%S %p')

# Display 5-day forecast
def displayForecast():
    location = locationEntry.get()
    forecastData = getForecast(location)

    if forecastData:
        forecastText = ""
        seenDates = set()

        for entry in forecastData["list"]:
            dateText = entry["dt_txt"].split(" ")[0]
            if dateText not in seenDates:
                seenDates.add(dateText)
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"]
                forecastText += f"{dateText}: {temp:.1f}° {'F' if units == 'imperial' else 'C'}, {desc.capitalize()}\n"

            if len(seenDates) == 5:
                break

        forecast.set(f"5-Day Forecast:\n{forecastText}")

# Toggle between Fahrenheit and Celsius
def toggleUnits():
    global units
    units = "metric" if units == "imperial" else "imperial"
    unitButton.config(text=f"Switch to {'Celsius' if units == 'imperial' else 'Fahrenheit'}")
    displayDetailedWeather()

# Clear displayed data
def clearData():
    locationEntry.delete(0, tk.END)
    detailedWeather.set("")
    forecast.set("")

# GUI Setup
app = tk.Tk()
app.title("Enhanced Python Weather App")

# Location Entry, ex. Bismarck, North Dakota
tk.Label(app, text="Enter location:").grid(row=0, column=0, padx=10, pady=10)
locationEntry = tk.Entry(app, width=20)
locationEntry.grid(row=0, column=1, padx=10, pady=10)

# Current Detailed Weather Display
detailedWeather = tk.StringVar()
tk.Label(app, textvariable=detailedWeather, justify="left").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Forecast Display
forecast = tk.StringVar()
tk.Label(app, textvariable=forecast, justify="left").grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Buttons
tk.Button(app, text="Get Detailed Weather", command=displayDetailedWeather).grid(row=3, column=0, padx=10, pady=10)
tk.Button(app, text="Get 5-Day Forecast", command=displayForecast).grid(row=3, column=1, padx=10, pady=10)

# Toggle Units Button
unitButton = tk.Button(app, text="Switch to Celsius", command=toggleUnits)
unitButton.grid(row=4, column=0, padx=10, pady=10)

# Clear Data Button
tk.Button(app, text="Clear", command=clearData).grid(row=4, column=1, padx=10, pady=10)

# Start GUI loop
app.mainloop()