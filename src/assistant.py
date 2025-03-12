#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant
===============

This module contains the Assistant class, which listens to user queries and responds accordingly.

"""

import re
from datetime import datetime

import command_registery
from infra import clear_screen, listen
from voice_interface import VoiceInterface


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
        return listen

    def execute_query(self, query: str) -> None:
        """Processes the query string and runs the corresponding tasks
        Args:
            query (str): the query string obtained from speech input
        """
        if query is None:
            print("No query detected. Please provide an input.")

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
                        command_registery.start_scrolling(direction)
                    )
            elif "stop scrolling" in query:
                if self.__scrolling_thread is None:  # Only stop if already scrolling
                    return
                command_registery.stop_scrolling(
                    self.__scrolling_thread, self.__stop_scrolling_event
                )
                del self.__scrolling_thread
                self.__scrolling_thread = None
            elif re.search(r"scroll to (up|down|left|right|top|bottom)", query):
                command_registery.scroll_to(direction)
            elif re.search(r"scroll (up|down|left|right)", query):
                command_registery.simple_scroll(direction)
            else:
                print("Scroll command not recognized")

        else:
            command, executor = command_registery.INSTANCE.get_executor(query=query)

            if command is None:
                self.__voice_interface.speak("could not interpret the query")
            else:
                executor(query, self.__voice_interface)

    def close(self):
        """Close the VoiceInterface instance and delete other variables"""
        self.__voice_interface.close()
        del self.__voice_interface
        if self.__scrolling_thread:
            command_registery.stop_scrolling(
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
