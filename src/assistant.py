#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant
===============

This module contains the Assistant class, which listens to user queries and responds accordingly.

"""

import json
import re
import subprocess
from datetime import datetime

import commands
from commands.send_email import send_email
from commands.utils import load_email_config
from commands.brightness_control import brightness_control
from commands.volume_control import volume_control
from commands.weather_reporter import weather_reporter
from commands.voice_interface import VoiceInterface
from commands.news_reporter import fetch_news
from commands import scroller
from infra import clear_screen


LISTENING_ERROR = "Say that again please..."
MAX_FETCHED_HEADLINES = (
    10  # Maximum number of news headlines to fetch when news function is called
)


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
                        scroller.start_scrolling(direction)
                    )
            elif "stop scrolling" in query:
                if self.__scrolling_thread is None:  # Only stop if already scrolling
                    return
                scroller.stop_scrolling(
                    self.__scrolling_thread, self.__stop_scrolling_event
                )
                del self.__scrolling_thread
                self.__scrolling_thread = None
            elif re.search(r"scroll to (up|down|left|right|top|bottom)", query):
                scroller.scroll_to(direction)
            elif re.search(r"scroll (up|down|left|right)", query):
                scroller.simple_scroll(direction)
            else:
                print("Scroll command not recognized")
        elif "weather" in query:
            cities = re.findall(
                r"\b(?:of|in|at)\s+(\w+)", query
            )  # Extract the city name just after the word 'of'
            weather_reporter(self.__voice_interface, cities[0])
        elif "email" in query:
            query = query.lower()

            data = load_email_config()

            if data.get("server") == "smtp.example.com":
                self.__voice_interface.speak(
                    "Please setup email config file before sending mail."
                )
            else:
                self.__voice_interface.speak("who do you want to send email to?")
                receiver = None
                validEmail = False
                while not validEmail:
                    receiver = self.listen_for_query()

                    if receiver in data.get("contacts").keys():
                        print(
                            f"Receiver selected from contacts: {data.get("contacts").get(receiver)}"
                        )
                        receiver = data.get("contacts").get(receiver)
                        validEmail = True
                    elif re.match(
                        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", receiver
                    ):
                        validEmail = True
                    else:
                        self.__voice_interface.speak(
                            "Valid Email not provided or contact does not exists"
                        )

                self.__voice_interface.speak(
                    "What would be the subject of the message? "
                )
                subject = None
                while subject is None:
                    subject = self.listen_for_query()

                self.__voice_interface.speak("What would be the body of the email?")
                body = None
                while body is None:
                    body = self.listen_for_query()

                print(
                    f"Sender Address: {data.get("username")}\n"
                    f"Receiver address: {receiver}\n"
                    f"Subject: {subject}\n"
                    f"Body: {body}\n"
                )

                self.__voice_interface.speak("Do You Want to send this email?")
                response = None
                while response is None:
                    response = self.listen_for_query()
                if "yes" in response.lower() or "sure" in response.lower():
                    self.__voice_interface.speak("Sending the email")
                    send_email(self.__voice_interface, receiver, subject, body)
                else:
                    self.__voice_interface.speak("Request aborted by user")

        elif "brightness" in query:
            query = query.lower()

            value = re.findall(r"\b(100|[1-9]?[0-9])\b", query)
            if len(value) == 0:
                print("Please provide a value or input is out of range")
            else:
                value = min(max(0, int(value[0])), 100)
                if "set" in query:
                    brightness_control(value, False, False)
                else:
                    toDecrease = "decrease" in query or "reduce" in query
                    relative = "by" in query
                    brightness_control(value, relative, toDecrease)

        elif "volume" in query:
            query = query.lower()

            value = re.findall(r"\b(100|[1-9]?[0-9])\b", query)
            if len(value) == 0:
                print("Please provide a value or input is out of range")
            else:
                value = min(max(0, int(value[0])), 100)
                if "set" in query:
                    volume_control(value, False, False)
                else:
                    toDecrease = "decrease" in query or "reduce" in query
                    relative = "by" in query
                    volume_control(value, relative, toDecrease)

        elif "shutdown" in query or "shut down" in query:
            self.__voice_interface.speak("Are you sure you want to shut down your PC?")
            response = None
            while response is None:
                response = self.listen_for_query()
            if "yes" in response.lower() or "sure" in response.lower():
                self.__voice_interface.speak("Shutting Down your PC")
                subprocess.run(["shutdown", "-s", "/t", "1"])
            else:
                self.__voice_interface.speak("Request aborted by user")

        elif "restart" in query:
            self.__voice_interface.speak("Are you sure you want to restart your PC?")
            response = None
            while response is None:
                response = self.listen_for_query()
            if "yes" in response.lower() or "sure" in response.lower():
                self.__voice_interface.speak("Restarting your PC")
                subprocess.run(["shutdown", "/r", "/t", "1"])
            else:
                self.__voice_interface.speak("Request aborted by user")
        elif "news" in query:
            fetch_news(self.__voice_interface, MAX_FETCHED_HEADLINES)

        else:
            self.__voice_interface.speak("could not interpret the query")

    def close(self):
        """Close the VoiceInterface instance and delete other variables"""
        self.__voice_interface.close()
        del self.__voice_interface
        if self.__scrolling_thread:
            scroller.stop_scrolling(
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
