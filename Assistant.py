#!/usr/bin/env python

import re, os, webbrowser
import pyttsx3, wikipedia
import speech_recognition as SR

from googlesearch import search
from datetime import datetime

from ExternalPath import AppPath, WebPath

def clrscr():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

class Assistant:
    def __init__(self) -> None:
        '''Creates an instance of the Voice-Assistant, initiates the engine, and assigns one of the preconfigured voice to it'''
        self.__engine = pyttsx3.init('sapi5')
        self.__engine.setProperty('voice', self.__engine.getProperty('voices')[2].id)
        
        self.__Terminate = False
        self.__recognizer = SR.Recognizer()
        
        self.__recognizer.energy_threshold = 200
        self.__recognizer.pause_threshold = 1
        self.__recognizer.phrase_threshold = 0.3
        self.__recognizer.non_speaking_duration = 0.5

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
        with SR.Microphone() as source:
            print("\nListening...")
            audio = self.__recognizer.listen(source)
        try: 
            print("Recognizing...\n")
            query = self.__recognizer.recognize_google(audio, language="en-in") # language = English(en)-India(in)
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
        
        if any( text in query for text in ['exit', 'quit', 'close'] ):
            self.__Terminate = True
        
        elif re.search(r'search .* in google', query):
            # Search the given query in google. uses googlesearch modules search function to get some results.
            # default is 10 results. It returns a generator which we convert to a list before showing to user.
            searchQuery = re.findall(r'search (.*) in google', query)[0]
            
            if not searchQuery:
                self.__speak("Invalid Google Search Query Found!!")
                return
            
            results = search(term=searchQuery) # googlesearch.search
            if results:
                results = list(results)
                self.__speak("Found Following Results: ")
                
                for i in range(len(results)):
                    print(i+1, ")", results[i])
            else:
                self.__speak("No Search Result Found!!")
                    
        elif 'wikipedia' in query:
            # searches wikipedia for the given query. Uses wikipedia module. The summary function returns a brief info about the searched query.
            # The number of sentences returned are set as 3. The value however can be changed
            # Error handling for DisambiguationError is provided which occurs when there are more than one related pages found.
            # The error message returns a string containing all the possible pages seperated by newline character.
            try:
                query = query.replace('wikipedia', "")
                self.__speak('Searching Wikipedia...')
                results = wikipedia.summary(query,  sentences=3)
                
                self.__speak("According to Wikipedia...")
                self.__speak(results)
            except wikipedia.exceptions.DisambiguationError as DE:
                self.__speak(f"\nError Found: {DE.__class__.__name__}")
                
                options = str(DE).split("\n")
                if len(options) < 7:
                    for option in options:
                        self.__speak(option)
                else:
                    for option in options[:6]:
                        self.__speak(option)
                    self.__speak("... and more")
            
        elif re.search('open .*', query):
            # Executes open application or url queries. 
            # Checks if application is present in the app dictionary and opens corresponding file if found.
            # Checks if application is present in the url dictionary and opens the corresponding link if found.
            # If not found as application or url, notifies the user as could not resolve application. 
            
            application = re.findall(r'open (.*)', query)[0]
            
            self.__speak(f"Attempting to open {application}....")
            if application in AppPath.keys():
                try:
                    os.startfile(AppPath[application.strip()])
                except:
                    self.__speak(f"Sorry! Failed to open {application}")
            elif application in WebPath.keys():
                try:
                    webbrowser.open_new(WebPath[application])
                except:
                    self.__speak(f"Sorry! Failed to open {application}")
            else:
                self.__speak(f"Oops! Couldn't resolve {application}")
                    
            
        elif 'the time' in query:
            date_time = datetime.now()
            hour, minute, second = date_time.hour, date_time.minute, date_time.second
            self.__speak(f"Current time is {hour}:{minute}:{second}")
        
        else:
            self.__speak('could not interprete the query')
        
           
    def run(self):
        '''Initiates the assistant listening and executing query process in a loop until user asks to exit'''
        self.__wishUser()
        clrscr()
        while not self.__Terminate:
            query = self.__listenQuery()
            self.__executeQuery( query )


    def setProperties(self, energy_threshold:int|None=None, pause_threshold:float|None=None, phrase_threshold:float|None=None, non_speaking_duration:float|None=None):
        '''
        Set properties for the listening

        - energy_threshold: Minimum audio energy to consider for recording (default = 200)
        - pause_threshold: Seconds of non-speaking audio to conclude a phrase (default = 1)
        - phrase_threshold: Minimum seconds of speaking required to be considered as a phrase (audio with time less than this are ignored to rule out clicks and pops) (default = 0.3)
        - non_speaking_duration: seconds of non-speaking audio to keep on both the sides of the recording (default = 0.5)
        '''
        if energy_threshold:
            self.__recognizer.energy_threshold = energy_threshold
        if pause_threshold:
            self.__recognizer.pause_threshold = pause_threshold
        if phrase_threshold:
            self.__recognizer.phrase_threshold = phrase_threshold
        if non_speaking_duration:
            self.__recognizer.non_speaking_duration = non_speaking_duration
            
             
    
    def close(self):
        '''Deletes the assistant's voice engine, recorder (recognizer) and the rest of the variables'''
        del self.__engine
        del self.__recognizer
        del self.__Terminate
    

if __name__ == "__main__":
    assistant = Assistant()
    assistant._Assistant__executeQuery(assistant._Assistant__listenQuery())
    #assistant.run()
    assistant.close()