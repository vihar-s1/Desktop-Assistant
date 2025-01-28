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
import wikipedia
from PIL import ImageGrab

from infra import __is_darwin, __is_posix, __is_windows, __system_os
from voice_interface import VoiceInterface

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


def fetch_news(vi: VoiceInterface) -> None:
    """News Reporter fetches headlines from news.google.com rss feed and reads top 5 headlines"""

    feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    max_fetched_headlines = 5

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