import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

def get_weather_by_gps(latitude, longitude, api_key):
    """
    Fetch the current weather for a given GPS location using WeatherAPI.

    Parameters:
    latitude (float): Latitude of the location
    longitude (float): Longitude of the location
    api_key (str): Your WeatherAPI key

    Returns:
    dict: Weather details or an error message
    """
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': f"{latitude},{longitude}",
        'aqi': 'no'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        weather_data = response.json()

        weather_info = {
            'Latitude': weather_data['location']['lat'],
            'Longitude': weather_data['location']['lon'],
            'Temperature (C)': weather_data['current']['temp_c'],
            'Condition': weather_data['current']['condition']['text'],
            'Humidity (%)': weather_data['current']['humidity'],
            'Wind Speed (kph)': weather_data['current']['wind_kph']
        }

        return weather_info

    except requests.exceptions.HTTPError as http_err:
        return {'error': f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {'error': f"Other error occurred: {err}"}
