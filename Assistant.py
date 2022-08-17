#!/usr/bin/env python

from datetime import datetime
from os import system
import re
import webbrowser
import pyttsx3
import speech_recognition as SR
import wikipedia
import googlesearch

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
        
        if any( text in query for text in ['exit', 'quit'] ):
            self.__Terminate = True
        
        elif re.match(r'search .* in google', query):
            searchQuery = re.findall(r'search (.*) in google', query)[0]
            
            if not searchQuery:
                self.__speak("Invalid Google Search Query Found!!")
                return
            
            results = googlesearch.search(term=searchQuery)
            if results:
                results = list(results)
                self.__speak("Found Following Results: ")
                
                for i in range(len(results)):
                    print(i+1, ")", results[i])
            else:
                self.__speak("No Search Result Found!!")
                    
        elif 'wikipedia' in query:
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
                       
        elif 'open youtube' in query:
            self.__speak('opening youtube in chrome...')
            webbrowser.open_new('https://www.youtube.com')
            
        elif 'open chrome' in query:
            self.__speak('opening chrome...')
            webbrowser.open_new('https://www.google.com')
            
        elif 'open google' in query:
            query = query.replace('open google', "")
            webbrowser.open_new('https://www.google.com')   
        
        else:
            self.__speak('could not interprete the query')
        
           
    def run(self):
        '''Initiates the assistant listening and executing query process in a loop until user asks to exit'''
        system("clear")
        self.__wishUser()
        while not self.__Terminate:
            self.__executeQuery( self.__listenQuery() )


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
    assistant._Assistant__executeQuery("search  in google")
    assistant.close()