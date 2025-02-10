#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic Features
===============

This module contains basic features for the desktop assistant, including:

- Explaining supported features
- Running Google search queries
- Telling the current time
- Performing Wikipedia searches

Functions:
    explain_features(vi: VoiceInterface) -> None:
        Explains the features available.

    run_search_query(vi: VoiceInterface, search_query: str) -> None:
        Performs a Google search based on some terms.

    tell_time(vi: VoiceInterface) -> None:
        Tells the current time of the day with timezone.

    wikipedia_search(vi: VoiceInterface, search_query: str, sentence_count: int = 3) -> None:
        Searches Wikipedia for the given query and returns a fixed number of sentences in response.
"""

from datetime import datetime

import googlesearch
import wikipedia

from .voice_interface import VoiceInterface

SUPPORTED_FEATURES = {
    "search your query in google and return upto 10 results",
    "get a wikipedia search summary of upto 3 sentences",
    "open applications or websites",
    "tell you the time of the day",
    "scroll the screen with active cursor",
}


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


def tell_time(vi: VoiceInterface) -> None:
    """Tells the time of the day with timezone

    Args:
        vi (VoiceInterface): Voice interface instance used to speak
    """
    date_time = datetime.now()
    hour, minute, second = date_time.hour, date_time.minute, date_time.second
    tmz = date_time.tzname()

    vi.speak(f"Current time is {hour}:{minute}:{second} {tmz}")


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
