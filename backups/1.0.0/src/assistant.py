#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant
===============

This module contains the Assistant class, which listens to user queries and responds accordingly.

"""

import re
from datetime import datetime

import commands
from infra import clear_screen
from voice_interface import VoiceInterface

LISTENING_ERROR = "Say that again please..."


class Assistant:
    """
    Assistant class containing implementation of the Assistant to listen and respond to user queries
    """

    def __init__(self):
        """Creates an Assistant instance consisting of a VoiceInterface instance"""
        self.__voice_interface = VoiceInterface()
        self.__scrolling_thread = None
        self.__stop_scrolling_event = None

    def wish_user(self):
        """Wishes user based on the hour of the day"""
        hour = int(datetime.now().hour)
        if 0 <= hour < 12:
            self.__voice_interface.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.__voice_interface.speak("Good Afternoon!")
        else:
            self.__voice_interface.speak("Good Evening!")

    def listen_for_query(self) -> str:
        """Listens for microphone input and return string of the input

        Returns:
            str: the query string obtained from the speech input
        """
        query = self.__voice_interface.listen(True)
        if query:
            print(f"User:\n{query}\n")
            self.__voice_interface.speak(query)
        else:
            print(LISTENING_ERROR)
            self.__voice_interface.speak(LISTENING_ERROR)
        return query

    def execute_query(self, query: str) -> None:
        """Processes the query string and runs the corresponding tasks
        Args:
            query (str): the query string obtained from speech input
        """
        if query is None:
            print("No query detected. Please provide an input.")

        elif "what can you do" in query:
            commands.explain_features(self.__voice_interface)

        elif re.search(r"search .* (in google)?", query):
            # to convert to a generalized format
            query = query.replace(" in google", "")
            search_query = re.findall(r"search (.*)", query)[0]
            commands.run_search_query(self.__voice_interface, search_query)

        elif "wikipedia" in query:
            # replace it only once to prevent changing the query
            query = query.replace("wikipedia", "", 1)
            search_query = query.replace("search", "", 1)
            commands.wikipedia_search(self.__voice_interface, search_query, 3)

        elif re.search("open .*", query):
            application = re.findall(r"open (.*)", query)
            if len(application) == 0:
                self.__voice_interface.speak("Which Application Should I Open ?")
                return
            application = application[0]
            try:
                commands.open_application_website(self.__voice_interface, application)
            except ValueError as ve:
                print(
                    f"Error occurred while opening {application}: {ve.__class__.__name__}: {ve}"
                )
                self.__voice_interface.speak(
                    f"Failed to open {application}. Please try again."
                )

        elif any(text in query for text in ["the time", "time please"]):
            commands.tell_time(self.__voice_interface)

        elif "scroll" in query:
            direction = re.search(r"(up|down|left|right|top|bottom)", query)
            if direction is None:
                print("Scroll direction not recognized")
                return
            direction = direction.group(0)

            if re.search(r"start scrolling (up|down|left|right|top|bottom)", query):
                if (
                    self.__scrolling_thread is None
                ):  # Only start if not already scrolling
                    self.__scrolling_thread, self.__stop_scrolling_event = (
                        commands.start_scrolling(direction)
                    )
            elif "stop scrolling" in query:
                if self.__scrolling_thread is None:  # Only stop if already scrolling
                    return
                commands.stop_scrolling(
                    self.__scrolling_thread, self.__stop_scrolling_event
                )
                del self.__scrolling_thread
                self.__scrolling_thread = None
            elif re.search(r"scroll to (up|down|left|right|top|bottom)", query):
                commands.scroll_to(direction)
            elif re.search(r"scroll (up|down|left|right)", query):
                commands.simple_scroll(direction)
            else:
                print("Scroll command not recognized")

        else:
            self.__voice_interface.speak("could not interpret the query")

    def close(self):
        """Close the VoiceInterface instance and delete other variables"""
        self.__voice_interface.close()
        del self.__voice_interface
        if self.__scrolling_thread:
            commands.stop_scrolling(
                self.__scrolling_thread, self.__stop_scrolling_event
            )
            del self.__scrolling_thread
        if self.__stop_scrolling_event:
            del self.__stop_scrolling_event

    def reset(self):
        """Re-instantiate VoiceInterface instance and other variables"""
        self.close()
        self.__voice_interface = VoiceInterface()
        self.__scrolling_thread = None
        self.__stop_scrolling_event = None


def __main__():
    assistant = Assistant()
    assistant.wish_user()
    clear_screen()
    while True:
        query = assistant.listen_for_query()
        assistant.execute_query(query)


if __name__ == "__main__":
    __main__()
