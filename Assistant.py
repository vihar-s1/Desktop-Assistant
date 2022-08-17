#!/usr/bin/env python

from datetime import datetime
import re
import webbrowser
import pyttsx3
import speech_recognition as SR
import wikipedia
from googlesearch import search

class Assistant:
    def __init__(self) -> None:
        '''Creates an instance of the Voice-Assistant, initiates the engine, and assigns one of the preconfigured voice to it'''
        self.__engine = pyttsx3.init('sapi5')
        self.__engine.setProperty('voice', self.__engine.getProperty('voices')[2].id)
        self.__Terminate = False

    def __speak(self, text):
        '''Tells Assistant to speak the given text and also prints on the console'''
        self.__engine.say(text)
        print(f"Assistant: {text}\n")
        self.__engine.runAndWait()
        
    def __wishUser(self):
        '''Wishes user based on the hour of the day and asks how it can help'''
        hour = int(datetime.now().hour)
        if  0 <= hour < 12:
            self.__speak("Good Morning!")
        elif 12 <= hour < 18:
            self.__speak("Good Afternoon!")
        else:
            self.__speak("Good Evening!")
        self.__speak("How Can I Help You ?")
        
    def __listenQuery(self):
        '''Listens for microphone input and returns string of the input'''
        recognizer = SR.Recognizer()
        with SR.Microphone() as source:
            print("\nListening...")
            recognizer.pause_threshold = 1 # Minimum no-audio time to consider phrase complete (default is 0.8)
            recognizer.energy_threshold = 200
            audio = recognizer.listen(source)
        try: 
            print("Recognizing...\n")
            query = recognizer.recognize_google(audio, language="en-in") # language = English(en)-India(in)
            query = query
            print(f"user said: {query}")
        except:
            self.__speak("Say that again please...")
            return None
            
        return query.lower()
    
    def __executeQuery(self, query: str):
        '''Runs the given query based on certain predefined conditions'''
        if not query:
            return
        
        if any( text in query for text in ['exit assistant', 'quit assistant'] ):
            self.__Terminate = True
        
           
    def run(self):
        self.__wishUser()
        while not self.__Terminate:
            self.__executeQuery( self.__listenQuery() )



if __name__ == "__main__":
    assistant = Assistant()
    assistant.run()