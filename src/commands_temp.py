#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Features
===============

This module contains all the functions pertaining to implementing the
individual features of the Assistant.

"""


import subprocess
import threading
import time
from datetime import datetime
from subprocess import CalledProcessError, TimeoutExpired

import feedparser
import googlesearch
import pyautogui as pag
import pygetwindow
import requests
import wikipedia

from comtypes import CLSCTX_ALL
from PIL import ImageGrab
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from commands.utils import load_email_config
from commands.voice_interface import VoiceInterface
from infra import __is_darwin, __is_posix, __is_windows, __system_os

SUPPORTED_FEATURES = {
    "search your query in google and return upto 10 results",
    "get a wikipedia search summary of upto 3 sentences",
    "open applications or websites",
    "tell you the time of the day",
    "scroll the screen with active cursor",
}

########## Conditional Imports ##########
if __is_windows():
    from AppOpener import open as open_app
########## Conditional Imports ##########

ENVIRONMENT_VARIABLES = dotenv_values(".env")


def explain_features(vi: VoiceInterface) -> None:
    """Explains the features available

    Args:
        vi (VoiceInterface): The voice interface instance used to speak the text
    """
    vi.speak("Here's what I can do...\n")
    for feature in SUPPORTED_FEATURES:
        vi.speak(f"--> {feature}")


def run_search_query(vi: VoiceInterface, search_query: str) -> None:
    """Performs google search based on some terms

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak
        search_query (str): the query term to be searched in google
    """
    if not search_query:
        vi.speak("Invalid Google Search Query Found!!")
        return

    results = googlesearch.search(term=search_query)
    if not results:
        vi.speak("No Search Result Found!!")
    else:
        results = list(results)
        vi.speak("Found Following Results: ")
        for i, result in enumerate(results):
            print(i + 1, ")", result.title)


def wikipedia_search(
    vi: VoiceInterface, search_query: str, sentence_count: int = 3
) -> None:
    """Searches wikipedia for the given query and returns fixed number of statements in response.
    Disambiguation Error due to multiple similar results is handled.
    Speaks the options in this case.

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The query term to search in wikipedia
        sentence_count (int, optional): The number of sentences to speak in case of direct match.
            Default is 3.
    """
    try:
        vi.speak("Searching Wikipedia...")
        results = wikipedia.summary(search_query, sentences=sentence_count)

        vi.speak("According to wikipedia...")
        vi.speak(results)
    except wikipedia.DisambiguationError as de:
        vi.speak(f"\n{de.__class__.__name__}")
        options = str(de).split("\n")
        if len(options) < 7:
            for option in options:
                vi.speak(option)
        else:
            for option in options[0:6]:
                vi.speak(option)
            vi.speak("... and more")


def open_application_website(vi: VoiceInterface, search_query: str) -> None:
    """
    open the application/website using a matching path from AppPath/WebPath dictionaries.

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The website or application name

    Raises:
        ValueError: Throws exception in case neither app nor web access-point is present.
    """
    vi.speak(f"Attempting to open {search_query}...")

    search_query = search_query.strip().lower()

    # use appopener to open the application only if os is windows
    if __is_windows():
        __open_application_website_windows(vi, search_query)
    if __is_darwin():
        __open_application_website_darwin(vi, search_query)
    elif __is_posix():
        __open_application_website_posix(vi, search_query)
    else:
        raise ValueError(f"Unsupported OS: {__system_os()}")


def __open_application_website_windows(vi: VoiceInterface, search_query: str) -> None:
    """handle the opening of application/website for Windows OS

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The website or application name

    Raises:
        ValueError: Throws exception in case neither app nor web access-point is present.
    """
    try:
        open_app(search_query, match_closest=True)  # attempt to open as application
    except Exception as error:
        vi.speak(f"Error: {error}: Failed to open {search_query}")


def __open_application_website_darwin(vi: VoiceInterface, search_query: str) -> None:
    """handle the opening of application/website for Darwin OS

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The website or application name

    Raises:
        ValueError: Throws exception in case neither app nor web access-point is present.
    """
    try:
        subprocess.run(
            ["open", "-a", search_query], capture_output=True, check=True
        )  # attempt to open as application
    except CalledProcessError:
        try:
            subprocess.run(
                ["open", search_query], capture_output=True, check=True
            )  # attempt to open as website
        except CalledProcessError as error:
            return_code = error.returncode
            stdout_text = error.stdout.decode("utf-8")
            stderr_text = error.stderr.decode("utf-8")
            vi.speak(
                f"Error: {error}: Failed to open {search_query}: error code {return_code}"
            )
            if stdout_text:
                print("stdout:", stdout_text)
            if stderr_text:
                print("stderr:", stderr_text)
        except TimeoutExpired as error:
            vi.speak(f"Error: {error}: Call to open {search_query} timed out.")

    except TimeoutExpired as error:
        vi.speak(f"Error: {error}: Call to open {search_query} timed out.")


def __open_application_website_posix(vi: VoiceInterface, search_query: str) -> None:
    """handle the opening of application/website for POSIX OS

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The website or application name

    Raises:
        ValueError: Throws exception in case neither app nor web access-point is present.
    """
    try:
        subprocess.run(
            ["xdg-open", search_query], capture_output=True, check=True
        )  # attempt to open website/application
    except CalledProcessError as error:
        vi.speak(
            f"Error: {error}: Failed to open {search_query}: error code {error.returncode}"
        )
        stdout_text = error.stdout.decode("utf-8")
        stderr_text = error.stderr.decode("utf-8")
        if stdout_text:
            print("stdout:", stdout_text)
        if stderr_text:
            print("stderr:", stderr_text)

    except TimeoutExpired as error:
        vi.speak(f"Error: {error}: Call to open {search_query} timed out.")


def tell_time(vi: VoiceInterface) -> None:
    """Tells the time of the day with timezone

    Args:
        vi (VoiceInterface): Voice interface instance used to speak
    """
    date_time = datetime.now()
    hour, minute, second = date_time.hour, date_time.minute, date_time.second
    tmz = date_time.tzname()

    vi.speak(f"Current time is {hour}:{minute}:{second} {tmz}")


def start_gradual_scroll(direction: str, stop_event: threading.Event) -> None:
    """Gradually scroll in the given direction until stop_event is set."""
    active_window = pygetwindow.getActiveWindow()
    if not active_window:
        return

    # Capture a portion of the window to ensure scrolling
    left, top, right, bottom = 0, 0, 100, 100
    width = right - left
    height = bottom - top
    previous_image = ImageGrab.grab(bbox=(left, top, left + width, top + height))
    while not stop_event.is_set():
        pag.scroll(clicks=1)
        current_image = ImageGrab.grab(bbox=(left, top, left + width, top + height))

        if current_image.getdata() == previous_image.getdata():
            print("Reached to extreme")
            stop_event.set()
            break
        previous_image = current_image

    print(f"Stopped scrolling {direction}.")


def start_scrolling(direction: str) -> tuple[threading.Thread, threading.Event]:
    """Start a new scroll thread."""
    stop_scrolling_event = threading.Event()
    scrolling_thread = threading.Thread(
        target=start_gradual_scroll, args=(direction, stop_scrolling_event)
    )
    scrolling_thread.start()
    return scrolling_thread, stop_scrolling_event


def stop_scrolling(
    scrolling_thread: threading.Thread, scrolling_thread_event: threading.Event
) -> None:
    """Stop the scrolling thread if not already stopped."""
    if scrolling_thread is not None:
        scrolling_thread_event.set()
        scrolling_thread.join()


def scroll_to(direction: str) -> None:
    """Scroll to the extreme in the given direction."""
    active_window = pygetwindow.getActiveWindow()
    if not active_window:
        return
    time.sleep(0.5)
    if direction == "top":
        pag.press("home")
    elif direction == "bottom":
        pag.press("end")
    elif direction == "right":
        pag.press("right", presses=9999)
    elif direction == "left":
        pag.press("left", presses=9999)
    else:
        print("Invalid Command")


def simple_scroll(direction: str) -> None:
    """Simple scroll in the given direction by a fixed number of steps."""
    active_window = pygetwindow.getActiveWindow()
    if not active_window:
        return
    time.sleep(0.5)
    if direction in ["up", "down", "left", "right"]:
        pag.press(keys=direction, presses=25)
    else:
        print("Invalid direction")


def volume_control(value: int, relative: bool, toDecrease: bool):
    """
    Adjusts the master volume of the system.

    Args:
        value (int): The volume level to set or adjust by. Should be between 0 and 100.
        relative (bool): If True, the volume change is relative to the current volume.
                         If False, the volume is set to the specified value.
        toDecrease (bool): If True, decreases the volume by the specified value.
                           If False, increases the volume by the specified value. Only applicable when `relative` is True.

    Raises:
        RuntimeError: If there is an issue with accessing the audio endpoint.

    Returns:
        None
    """

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    if relative:
        current_volume = volume.GetMasterVolumeLevelScalar() * 100
        set_volume = (
            current_volume - int(value) if toDecrease else current_volume + int(value)
        )
        print(set_volume)
        volume.SetMasterVolumeLevelScalar(min(max(0, set_volume), 100) / 100, None)
    else:
        volume.SetMasterVolumeLevelScalar(min(max(0, value), 100) / 100, None)


def fetch_news(vi: VoiceInterface, max_fetched_headlines: int) -> None:
    """
    Fetches and reads out the top 5 headlines from the Google News RSS feed.

    This function fetches news headlines from the Google News RSS feed (specific to India in English).
    It then reads out the top 5 headlines using the provided VoiceInterface instance. If the feed fetch is successful,
    it reads the headlines one by one. If the fetch fails, it informs the user that the news couldn't be fetched.

    Args:
        vi (VoiceInterface): The VoiceInterface instance used to speak the news headlines.

    Raises:
        requests.exceptions.RequestException: If there is an issue while fetching the RSS feed.
        AttributeError: If the feed does not contain expected attributes or entries.
    """

    feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"

    vi.speak("Fetching news from servers.")
    feed = feedparser.parse(feed_url)
    if feed.status == 200:
        headlines_list = []
        for entry in feed.entries[:max_fetched_headlines]:
            headlines_list.append((entry.title).split(" -")[0])
        vi.speak("Here are some recent news headlines.")
        for headline in headlines_list:
            vi.speak(headline)
    else:
        vi.speak("Failed to fetch the news.")


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
