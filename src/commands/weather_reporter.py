import re

import requests

from voice_interface import VoiceInterface


class WeatherReporter:

    @staticmethod
    def command_name() -> str:
        return WeatherReporter.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return "weather" in query

    @staticmethod
    def execute_query(query: str, vi: VoiceInterface) -> None:
        # Extract the city name just after the word 'of'
        cities = re.findall(r"\b(?:of|in|at)\s+(\w+)", query)
        weather_reporter(vi, cities[0])


def weather_reporter(vi: VoiceInterface, city_name: str) -> None:
    # Fetch latitude and longitude for the given city to be used by open-metro api
    params = {
        "name": city_name,
    }
    geo_codes = requests.get(
        "https://api.api-ninjas.com/v1/city",
        params=params,
        headers={"origin": "https://www.api-ninjas.com"},
    ).json()

    query_params = {
        "latitude": geo_codes[0].get("latitude"),
        "longitude": geo_codes[0].get("longitude"),
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,rain,showers,cloud_cover,wind_speed_10m",
        "forecast_days": 1,
    }

    # Fetch weather data from Open-Meteo using the obtained coordinates. Time out after 60 seeconds of no response
    weather_data_response = requests.get(
        "https://api.open-meteo.com/v1/forecast", params=query_params, timeout=60
    ).json()

    weather_data = weather_data_response.get("current")
    weather_units = weather_data_response.get("current_units")

    vi.speak(
        f"The current temperature in {city_name} is {weather_data.get('temperature_2m')}{weather_units.get('temperature_2m')}. "
        f"However, due to a relative humidity of {weather_data.get('relative_humidity_2m')}{weather_units.get('relative_humidity_2m')}, "
        f"it feels like {weather_data.get('apparent_temperature')}{weather_units.get('apparent_temperature')}."
    )

    if weather_data.get("rain") == 0:
        vi.speak("The skies will be clear, with no chance of rain.")
    else:
        cloud_cover = weather_data.get("cloud_cover")
        vi.speak(
            f"The sky will be {cloud_cover}{weather_units.get('cloud_cover')} cloudy, "
            f"and there's a predicted rainfall of {weather_data.get('rain')}{weather_units.get('rain')}."
        )

    vi.speak(
        f"The wind speed is expected to be {weather_data.get('wind_speed_10m')}{weather_units.get('wind_speed_10m')}, "
        "so plan accordingly."
    )
