#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scroller
===============

This module contains functions to handle scrolling actions for the desktop assistant.

Functions:
    start_gradual_scroll(direction: str, stop_event: threading.Event) -> None:
        Gradually scrolls in the given direction until the stop_event is set.

    start_scrolling(direction: str) -> tuple[threading.Thread, threading.Event]:
        Starts a new thread to handle gradual scrolling.

    stop_scrolling(scrolling_thread: threading.Thread, scrolling_thread_event: threading.Event) -> None:
        Stops the scrolling thread if it is not already stopped.

    scroll_to(direction: str) -> None:
        Scrolls to the extreme in the given direction.

    simple_scroll(direction: str) -> None:
        Performs a simple scroll in the given direction by a fixed number of steps.
"""

import threading
import time

import pyautogui as pag
import pygetwindow
from PIL import ImageGrab


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
