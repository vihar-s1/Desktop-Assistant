import re, os, webbrowser
import wikipedia, googlesearch
from datetime import datetime

from Extras import AppPath, WebPath
from VoiceInterface import VoiceInterface
import Support

LISTENING_ERROR = "Say that again please..."

class Assistant:
    def __init(self) -> None:
        """Creates an Assistant instance consisting of an VoiceInterface instance"""
        self.__voiceInterface = VoiceInterface()
        
    
    def wishUser(self):
        """Wishes user based on the hour of the day"""
        hour = int (datetime.now().hour)
        if 0 <= hour < 12:
            self.__voiceInterface.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.__voiceInterface.speak("Good Afternoon!")
        else:
            self.__voiceInterface.speak("Good Evening!")
            
    
    def listenQuery(self) -> str:
        """Listens for microphone input and return string of the input

        Returns:
            str: the query string obtained from the speech input
        """
        query = self.__voiceInterface.listen(True)
        if query:
            print(f"User:\n{query}\n")
            self.__voiceInterface.speak(query)
        else:
            print(LISTENING_ERROR)
            self.__voiceInterface.speak(LISTENING_ERROR)
        return query
    
    
    def executeQuery(self, query: str) -> None:
        """Processes the query string and runs the corresponding tasks

        Args:
            query (str): the query string obtained from speech input
        """
        # if any( text in query for text in ['exit', 'quit', 'close'] ):
        #     return
        
        if 'what can you do' in query:
            Support.explainFeatures(self.__voiceInterface)
        
        elif re.match(r'[what|all|list].*apps.*open', query):
            Support.possibleAppsAndWebs(self.__voiceInterface)
        
        elif re.search(r'search .* (in google){0,1}', query):
            query.replace(" in google", "") # to convert to a generalized format
            searchQuery = re.findall(r'search (.*)', query)[0]
            Support.runSearchQuery(self.__voiceInterface, searchQuery)
            
        elif 'wikipedia' in query:
            # replace only once to prevent changing the query
            query = query.replace("wikipedia", "", 1)
            query = query.replace("search", "", 1)
            Support.wikipediaSearch(self.__voiceInterface, searchQuery, 3)
            
        elif re.search('open .*', query):
            application = re.findall(r"open (.*)", query)
            if len(application) == 0:
                self.__voiceInterface.speak("Which Application Should I Open ?")
                return
            application = application[0]
            try:
                Support.openApplicationWebsite(self.__voiceInterface, application)
            except ValueError:
                self.__voiceInterface.speak(f"Accesspoint Matching {application} not found !")
        
        elif any(text in query for text in ["the time", "time please"]):
            Support.tellTime(self.__voiceInterface)
            
        else:
            self.__voiceInterface.speak("could not interprete the query")
    
    
    def close(self):
        """Close the VoiceInterface instance and delete other variables"""
        self.__voiceInterface.close()
        del self.__voiceInterface
        
    
    def reset(self):
        """Re-instantiate VoiceInterface instance and other variables"""
        if self.__voiceInterface:
            self.__voiceInterface.close()
            del self.__voiceInterface
        self.__voiceInterface = VoiceInterface()
        

def __main__():
    assistant = Assistant()
    assistant.wishUser()
    Support.clrscr()
    while True:
        query = assistant.listenQuery()
        assistant.executeQuery(query)


if __name__ == "__main__":
    __main__()