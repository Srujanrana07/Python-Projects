import os
import requests
from dotenv import load_dotenv


load_dotenv()

def get_weather(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
        return weather
    else:
        print("Error fetching weather data.")
        return None

def main():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if api_key is None:
        print("OpenWeatherMap API key not found in .env file.")
        return

    location = input("Enter city name: ")

    weather = get_weather(api_key, location)

    if weather:
        print(f"Weather in {location}:")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Description: {weather['description']}")
    else:
        print("No weather data available.")

if __name__ == "__main__":
    main()
