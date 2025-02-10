import requests
from .voice_interface import VoiceInterface


def weather_reporter(vi: VoiceInterface, city_name: str) -> None:
    """
    Fetches and reports the weather conditions for a given city.

    This function retrieves the latitude and longitude of the specified city using the API Ninjas City API.
    It then fetches the current weather data from the Open-Meteo API and reports the temperature, humidity,
    apparent temperature, rain probability, cloud cover, and wind speed using the VoiceInterface instance.

    Args:
        vi (VoiceInterface): The VoiceInterface instance used to speak the weather report.
        city_name (str): The name of the city for which to fetch weather data.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the API request.
        IndexError: If the city name is not found in the API response.
        KeyError: If expected weather data fields are missing from the response.
    """
    # Fetch latitude and longitude for the given city to be used by open-metro api
    params = {
        "name": city_name,
    }
    geo_codes = requests.get(
        "https://api.api-ninjas.com/v1/city",
        params=params,
        headers={"origin": "https://www.api-ninjas.com"},
    ).json()

    # Fetch weather data from Open-Meteo using the obtained coordinates
    weather_data_response = requests.get(
        f'https://api.open-meteo.com/v1/forecast?latitude={geo_codes[0].get("latitude")}&longitude={geo_codes[0].get("longitude")}&current=temperature_2m,relative_humidity_2m,apparent_temperature,rain,showers,cloud_cover,wind_speed_10m&forecast_days=1'
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
