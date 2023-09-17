#!/usr/bin/env python

import pyttsx3
from pyttsx3 import voice
import speech_recognition as SR
        

class VoiceInterface:
    """
    Class consisting of functions that allow speech-to-text
    and text-to-speech conversions.
    """
    def __init__(self) -> None:
        """
        Creates VoiceInterface instance consisting of an voice engine,
        sets the voice of the engine, and creates a voice recognizer instance.
        """
        self.__engine = pyttsx3.init('sapi5')
        self.__engine.setProperty('voice', self.__engine.getProperty('voices')[1].id)
        
        self.__recognizer = SR.Recognizer()
        self.__recognizer.energy_threshold = 150
        self.__recognizer.pause_threshold = 1
        self.__recognizer.phrase_threshold = 0.3
        self.__recognizer.non_speaking_duration = 0.5
        
    
    def speak(self, text: str) -> None:
        """Tells Assistant to speak the given 'text' and also prints on the console."""
        self.__engine.say(text)
        print(text)
        self.__engine.runAndWait()
        
    
    def listen(self, printStatement: bool = False) -> str:
        """
        Listens for Microphone input, converts to string using
        google recognization engine,and returns the string on success.
        """
        with SR.Microphone() as source:
            if printStatement: print("\nListening...")
            audio = self.__recognizer.listen(source)
        try:
            # language = Englist(en)-India(in)
            if printStatement: print("Recognizing...\n")
            query = self.__recognizer.recognize_google(audio_data=audio, language="en-in")
            return query
        except:
            return None
        
    
    def setProperties(self, energy_threshold:int|None=None, pause_threshold:float|None=None, phrase_threshold:float|None=None, non_speaking_duration:float|None=None) -> None:
        """Set properties of the (voice) recognizer instance

        Args:
            energy_threshold (int | None, optional):
                            Min audio energy for recording. Default value is 150.
            pause_threshold (float | None, optional):
                            Silence after a phrase to conclude recording. Default value is 1.
            phrase_threshold (float | None, optional):
                            Min audio time to be considered for recording. Default value is 0.3.
            non_speaking_duration (float | None, optional):
                            Empty Audio buffer on start and end of audio. Default value is 0.5.
        """
        if energy_threshold: self.__recognizer.energy_threshold = energy_threshold
        if pause_threshold: self.__recognizer.pause_threshold = pause_threshold
        if phrase_threshold: self.__recognizer.phrase_threshold = phrase_threshold
        if non_speaking_duration: self.__recognizer.non_speaking_duration = non_speaking_duration
        
    
    def getAvailableVoices(self) -> list[voice.Voice]:
        return self.__engine.getProperty('voices')
    
    
    def setVoice(self, voiceInstance: voice.Voice) -> None:
        if isinstance(voiceInstance, voice.Voice):
            self.__engine.setProperty('voice', voiceInstance.id)


    def close(self) -> None:
        """Deletes the Voice Engine and Recognizer instances"""
        self.speak("Have a Good Day !!!")
        del self.__engine
        del self.__recognizer