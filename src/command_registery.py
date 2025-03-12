#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Features
===============

This module contains all the functions pertaining to implementing the
individual features of the Assistant.

"""

import threading
import time

import pyautogui as pag
import pygetwindow
from dotenv import dotenv_values
from PIL import ImageGrab

from commands.brightness_control import BrightnessControl
from commands.current_time import CurrentTime
from commands.fetch_news import FetchNews
from commands.google_search import GoogleSearch
from commands.open_application import OpenApplication
from commands.restart_system import RestartSystem
from commands.send_email import SendEmail
from commands.shutdown_system import ShutdownSystem
from commands.volume_control import VolumeControl
from commands.weather_reporter import WeatherReporter
from commands.wikipedia_search import WikipediaSearch
from infra import __is_windows
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

ENVIRONMENT_VARIABLES = dotenv_values(".env")


def explain_features(vi: VoiceInterface) -> None:
    """Explains the features available

    Args:
        vi (VoiceInterface): The voice interface instance used to speak the text
    """
    vi.speak("Here's what I can do...\n")
    for feature in SUPPORTED_FEATURES:
        vi.speak(f"--> {feature}")


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


class CommandRegistery:
    """Class to register and execute commands based on the query"""

    def __init__(self, vi: VoiceInterface) -> None:
        self.vi = vi
        self.__registery = dict[str, tuple[callable, callable]]()

    def register_command(
        self, command: str, validateQuery: callable, executeQuery: callable
    ) -> None:
        """
        Registers a command with the CommandRegistery.

        Args:
            command (str): The command string to register.
            validateQuery (callable): The function to validate the query for the command.
            executeQuery (callable): The function to execute the query for the command.
        """
        self.__registery[command] = (validateQuery, executeQuery)

    def get_executor(self, query: str) -> tuple[str, callable]:
        """
        Returns the executor function for the given query.

        Args:
            query (str): The query to find the executor for.

        Returns:
            tuple[str, callable]: The command string and the executor function for the query.
        """
        for command, validateQuery, executeQuery in self.__registery:
            if validateQuery.__call__(query):
                return command, executeQuery
        return None, None

    def get_command(self, command: str) -> tuple[callable, callable]:
        """Get the query validator and query executor for given command name

        Args:
            command (str): name of the command to fetch

        Returns:
            tuple[callable, callable]: Tuple of Query Validator and Query Executor if found
        """
        if self.__registery is None:
            return None, None

        self.__registery.get(key=command, default=(None, None))


INSTANCE = CommandRegistery(VoiceInterface())

INSTANCE.register_command(
    GoogleSearch.commandName(), GoogleSearch.validateQuery, GoogleSearch.executeQuery
)
INSTANCE.register_command(
    WikipediaSearch.commandName(),
    WikipediaSearch.validateQuery,
    WikipediaSearch.executeQuery,
)
INSTANCE.register_command(
    OpenApplication.commandName(),
    OpenApplication.validateQuery,
    OpenApplication.executeQuery,
)
INSTANCE.register_command(
    CurrentTime.commandName(), CurrentTime.validateQuery, CurrentTime.executeQuery
)
INSTANCE.register_command(
    BrightnessControl.commandName(),
    BrightnessControl.validateQuery,
    BrightnessControl.executeQuery,
)
INSTANCE.register_command(
    VolumeControl.commandName(), VolumeControl.validateQuery, VolumeControl.executeQuery
)
INSTANCE.register_command(
    ShutdownSystem.commandName(),
    ShutdownSystem.validateQuery,
    ShutdownSystem.executeQuery,
)
INSTANCE.register_command(
    RestartSystem.commandName(), RestartSystem.validateQuery, RestartSystem.executeQuery
)
INSTANCE.register_command(
    WeatherReporter.commandName(),
    WeatherReporter.validateQuery,
    WeatherReporter.executeQuery,
)
INSTANCE.register_command(
    FetchNews.commandName(), FetchNews.validateQuery, FetchNews.executeQuery
)
INSTANCE.register_command(
    SendEmail.commandName(), SendEmail.validateQuery, SendEmail.executeQuery
)
