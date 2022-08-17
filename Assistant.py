#!/usr/bin/env python

from datetime import datetime
import pyttsx3

class Assistant:
    def __init__(self) -> None:
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('voice', self.engine.getProperty('voices')[2].id)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        
    def wishUser(self):
        hour = int(datetime.now().hour)
        if  0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("How Can I Help You ?")
        

if __name__ == "__main__":
    assistant = Assistant()
    assistant.wishUser()