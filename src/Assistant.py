import re
from datetime import datetime
import threading
import Support
from VoiceInterface import VoiceInterface

LISTENING_ERROR = "Say that again please..."

class Assistant:
    def __init__(self):
        """Creates an Assistant instance consisting of an VoiceInterface instance"""
        self.__voiceInterface = VoiceInterface()
        
        
    def wish_user(self):
        """Wishes user based on the hour of the day"""
        hour = int (datetime.now().hour)
        if 0 <= hour < 12:
            self.__voiceInterface.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.__voiceInterface.speak("Good Afternoon!")
        else:
            self.__voiceInterface.speak("Good Evening!")
            
    
    def listen_for_query(self) -> str:
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
    

    def execute_query(self, query: str) -> None:
        """Processes the query string and runs the corresponding tasks
        Args:
            query (str): the query string obtained from speech input
        """
        if query is None:
            print("No query detected. Please provide an input.")
        elif 'what can you do' in query:
            Support.explain_features(self.__voiceInterface)
        
        elif re.match(r'(what|all|list).*apps.*open', query):
            Support.possible_apps_and_webs(self.__voiceInterface)
        
        elif re.search(r'search .* (in google)?', query):
            query = query.replace(" in google", "") # to convert to a generalized format
            search_query = re.findall(r'search (.*)', query)[0]
            Support.run_search_query(self.__voiceInterface, search_query)
            
        elif 'wikipedia' in query:
            # replace only once to prevent changing the query
            query = query.replace("wikipedia", "", 1)
            search_query = query.replace("search", "", 1)
            Support.wikipedia_search(self.__voiceInterface, search_query, 3)
            
        elif re.search('open .*', query):
            application = re.findall(r"open (.*)", query)
            if len(application) == 0:
                self.__voiceInterface.speak("Which Application Should I Open ?")
                return
            application = application[0]
            try:
                Support.open_application_website(self.__voiceInterface, application)
            except ValueError:
                self.__voiceInterface.speak(f"Access point Matching {application} not found !")
        
        elif any(text in query for text in ["the time", "time please"]):
            Support.tell_time(self.__voiceInterface)
        
        elif 'scroll' in query:
            if re.search(r'start scrolling (up|down|left|right|top|bottom)', query):
                direction = re.findall(r'start scrolling (up|down|left|right|top|bottom)', query)[0]
                scroll_thread,stop_scroll_event=Support.setup_scrolling()
                if scroll_thread is None:  # Only start if not already scrolling
                    Support.start_scrolling(direction)

            elif 'stop scrolling' in query:
                scroll_thread,stop_scroll_event=Support.setup_scrolling()
                if scroll_thread is not None:
                    Support.stop_scrolling()  
            elif re.search(r'scroll to (up|down|left|right|top|bottom)', query):
                match = re.search(r'scroll to (up|down|left|right|top|bottom)', query)
                direction = match.group(1)
                Support.scroll_to(direction)
            elif re.search(r'scroll (up|down|left|right)', query):
                match = re.search(r'scroll (up|down|left|right)', query)
                direction = match.group(1)
                Support.simple_scroll(direction)
            else:
                print("Scroll command not recognized")     
        else:
            self.__voiceInterface.speak("could not interpret the query")
    
    
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
    assistant.wish_user()
    Support.clear_screen()
    while True:
        query = assistant.listen_for_query()
        assistant.execute_query(query)


if __name__ == "__main__":
    __main__()