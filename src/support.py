#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Support
===============

This module contains the functions that support the Assistant in performing various tasks.

"""

import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from subprocess import CalledProcessError, TimeoutExpired

import googlesearch
import pyautogui as pag
import pygetwindow as gw
import wikipedia
from AppOpener import open as open_app
from PIL import ImageGrab

from voice_interface import VoiceInterface

# include the actual code to gradual score
# TODO: Remove the global variables scroll thread and stop scroll event
SCROLL_THREAD = None
STOP_SCROLL_EVENT = threading.Event()

SUPPORTED_FEATURES = {
    "search your query in google and return upto 10 results",
    "get a wikipedia search summary of upto 3 sentences",
    "open applications or websites",
    "tell you the time of the day",
    "scroll the screen with active cursor",
}


def clear_screen() -> None:
    """Clears the screen based on the operating system"""
    if __is_windows__():
        os.system("cls")
    else:
        os.system("clear")


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
    if not isinstance(vi, VoiceInterface):
        raise ValueError(
            f"Argument 'vi' should be of type {VoiceInterface}, found {type(vi)}"
        )
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
    if __is_windows__():
        __open_application_website_windows__(vi, search_query)
    if __is_darwin__():
        __open_application_website_darwin__(vi, search_query)
    elif __is_posix__():
        __open_application_website_posix__(vi, search_query)
    else:
        raise ValueError(f"Unsupported OS: {__system_os__()}")


def __open_application_website_windows__(vi: VoiceInterface, search_query: str) -> None:
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


def __open_application_website_darwin__(vi: VoiceInterface, search_query: str) -> None:
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


def __open_application_website_posix__(vi: VoiceInterface, search_query: str) -> None:
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
    if not isinstance(vi, VoiceInterface):
        raise ValueError(
            f"Argument 'vi' should be of type {VoiceInterface}, found {type(vi)}"
        )

    date_time = datetime.now()
    hour, minute, second = date_time.hour, date_time.minute, date_time.second
    tmz = date_time.tzname()

    vi.speak(f"Current time is {hour}:{minute}:{second} {tmz}")


def setup_scrolling() -> tuple[threading.Thread | None, threading.Event]:
    """Set up the scrolling thread and "stop scroll" event if not already setup."""
    if not hasattr(setup_scrolling, "SCROLL_THREAD"):
        setup_scrolling.SCROLL_THREAD = None
    if not hasattr(setup_scrolling, "STOP_SCROLL_EVENT"):
        setup_scrolling.STOP_SCROLL_EVENT = threading.Event()

    return setup_scrolling.SCROLL_THREAD, setup_scrolling.STOP_SCROLL_EVENT


def start_gradual_scroll(direction: str, stop_event: threading.Event) -> None:
    """Gradually scroll in the given direction until stop_event is set."""
    time.sleep(2)
    active_window = pag.getActiveWindow()
    if active_window:

        left, top, width, height = (
            active_window.left,
            active_window.top,
            active_window.width,
            active_window.height,
        )

        previous_image = ImageGrab.grab(
            # Capture the entire window
            bbox=(left, top, left + width, top + height)
        )

        while True:
            if stop_event.is_set():
                break
            pag.press(direction)
            time.sleep(1)
            current_image = ImageGrab.grab(bbox=(left, top, left + width, top + height))

            if list(current_image.getdata()) == list(previous_image.getdata()):
                print("Reached to extreme")
                stop_event.set()
                setup_scrolling.SCROLL_THREAD = None
                break
            previous_image = current_image

        print(f"Scrolling {direction}...")  # Simulate scrolling action
        # Simulate delay between scroll actions
    print(f"Stopped scrolling {direction}.")


def start_scrolling(direction: str) -> None:
    """Start a new scroll thread."""
    setup_scrolling.STOP_SCROLL_EVENT.clear()
    setup_scrolling.SCROLL_THREAD = threading.Thread(
        target=start_gradual_scroll, args=(direction, setup_scrolling.STOP_SCROLL_EVENT)
    )
    setup_scrolling.SCROLL_THREAD.start()


def stop_scrolling() -> None:
    """Stop the current scrolling thread."""
    setup_scrolling.STOP_SCROLL_EVENT.set()
    if setup_scrolling.SCROLL_THREAD is not None:
        setup_scrolling.SCROLL_THREAD.join()
        setup_scrolling.SCROLL_THREAD = None
    print("Scrolling has stopped.")


def scroll_to(direction: str) -> None:
    """Scroll to the extreme in the given direction."""
    active_window = gw.getActiveWindow()
    if active_window:
        # Bring the active window to the front
        active_window.activate()
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


# pygetwindow and implement
def simple_scroll(direction: str) -> None:
    """Simple scroll in the given direction by a fixed number of steps."""
    active_window = gw.getActiveWindow()
    if active_window:
        # Bring the active window to the front
        # active_window.activate()
        time.sleep(0.5)
        if direction == "up":
            pag.press("up", presses=25)
        elif direction == "down":
            pag.press("down", presses=25)
        elif direction == "right":
            pag.press("right", presses=25)
        elif direction == "left":
            pag.press("left", presses=25)

        else:
            print("Invalid direction")


def __is_windows__() -> bool:
    """Returns True if the operating system is Windows"""
    return sys.platform in ["win32", "cygwin"]


def __is_darwin__() -> bool:
    """Returns True if the operating system is Darwin"""
    return sys.platform in ["darwin", "ios"]


def __is_posix__() -> bool:
    """Returns True if the operating system is POSIX"""
    return sys.platform in ["aix", "android", "emscripten", "linux", "darwin", "wasi"]


def __system_os__() -> str:
    """Returns the name of the operating system"""
    return sys.platform
