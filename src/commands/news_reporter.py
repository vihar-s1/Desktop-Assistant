#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News Reporter
===============

This module contains functions to fetch and read out the top news headlines.

Functions:
    fetch_news(vi: VoiceInterface, max_fetched_headlines: int) -> None:
        Fetches and reads out the top headlines from the Google News RSS feed.

        Args:
            vi (VoiceInterface): The VoiceInterface instance used to speak the news headlines.
            max_fetched_headlines (int): The maximum number of headlines to fetch and read out.

        Raises:
            requests.exceptions.RequestException: If there is an issue while fetching the RSS feed.
            AttributeError: If the feed does not contain expected attributes or entries.
"""
import feedparser

from .voice_interface import VoiceInterface


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
