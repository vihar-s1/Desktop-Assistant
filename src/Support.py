import os
from datetime import datetime
import threading
import time
import pyautogui as pag
import pygetwindow as gw
from PIL import ImageGrab

import googlesearch
import wikipedia

from ExternalPaths import AppPath, WebPath, features
from VoiceInterface import VoiceInterface
#include the actual code to gradual score
scroll_thread = None
stop_scroll_event = threading.Event()

def clear_screen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")
        
        
def possible_apps_and_webs(vi: VoiceInterface) -> None:
    vi.speak("Here is a list of all apps and websites I can open:")
    vi.speak("\n".join(AppPath.keys()))
    vi.speak("\n".join(WebPath.keys()))
    

def explain_features(vi: VoiceInterface) -> None:
    """Explains the features available

    Args:
        vi (VoiceInterface): The voice interface instance used to speak the text
    """
    vi.speak("Here's what I can do...\n")
    for feature in features:
        vi.speak(f"--> {feature}")
    

def run_search_query(vi: VoiceInterface, search_query: str) -> None:
    """Performs google search based on some terms

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak
        search_query (str): the query term to be searched in google
    """
    if not isinstance(vi, VoiceInterface):
        raise ValueError(f"Argument 'vi' should be of type {VoiceInterface}, found {type(vi)}")
    if not search_query:
        vi.speak("Invalid Google Search Query Found!!")
        return
    
    results = googlesearch.search(term=search_query)
    if not results: vi.speak("No Search Result Found!!")
    
    try:
        results = list(results)
        vi.speak("Found Following Results: ")
        for i in range(len(results)):
            print(i+1, ")", results[i])
    except Exception as error:
        print(error.__str__)
        

def wikipedia_search(vi: VoiceInterface, search_query: str, sentence_count:int=3) -> None:
    """Searches wikipedia for the given query and returns fixed number of statements in response.
    Disambiguation Error due to multiple similar results is handled. Speaks the options in this case.

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The query term to search in wikipedia
        sentence_count (int, optional): The number of sentences to speak in case of direct match. Defaults to 3.
    """
    try:
        vi.speak("Searching Wikipedia...")
        results = wikipedia.summary(search_query, sentences=sentence_count)
        
        vi.speak("According to wikipedia...")
        vi.speak(results)
    except wikipedia.DisambiguationError as DE:
        vi.speak(f"\n{DE.__class__.__name__}")
        options = str(DE).split("\n")
        if len(options) < 7:
            for option in options: vi.speak(option)
        else:
            for option in options[0:6]: vi.speak(option)
            vi.speak("... and more")
        

def open_application_website(vi: VoiceInterface, search_query: str) -> None:
    """Attempts to raise the application or website by finding the access-point in the AppPath/WebPath dictionaries

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The website or application name

    Raises:
        ValueError: Throws exception in case neither app nor web access-point is present.
    """
    vi.speak(f"Attempting to open {search_query}...")
    if search_query in AppPath.keys():
        try:  os.startfile(AppPath[search_query.strip()])
        except Exception as error:
            vi.speak(f"Error: {error}: Failed to open {search_query}")
        
    elif search_query in WebPath.keys():
        try:  os.startfile(WebPath[search_query.strip()])
        except Exception as error:
            vi.speak(f"Error: {error}: Failed to open {search_query}")
    
    else:
        raise ValueError(f"Missing Access-point for {search_query}")


def tell_time(vi: VoiceInterface) -> None:
    """Tells the time of the day with timezone

    Args:
        vi (VoiceInterface): Voice interface instance used to speak
    """
    if not isinstance(vi, VoiceInterface):
        raise ValueError(f"Argument 'vi' should be of type {VoiceInterface}, found {type(vi)}")
    
    date_time = datetime.now()
    hour, minute, second = date_time.hour, date_time.minute, date_time.second
    tmz = date_time.tzname()
    
    vi.speak(f"Current time is {hour}:{minute}:{second} {tmz}")

def setup_scrolling():
      if not hasattr(setup_scrolling, "scroll_thread"):
        setup_scrolling.scroll_thread = None
      if not hasattr(setup_scrolling, "stop_scroll_event"):
        setup_scrolling.stop_scroll_event = threading.Event()

      return setup_scrolling.scroll_thread, setup_scrolling.stop_scroll_event

def start_gradual_scroll(direction: str, stop_event: threading.Event) -> None:
    """Gradually scroll in the given direction until stop_event is set."""
    time.sleep(2)
    active_window = pag.getActiveWindow()
    if active_window:
    
        left, top, width, height = active_window.left, active_window.top, active_window.width, active_window.height
        
        previous_image = ImageGrab.grab(bbox=(left, top, left + width, top + height))  # Capture the entire window

        while True:
            if stop_event.is_set():
                break
            pag.press(direction)  
            time.sleep(1)  
            current_image = ImageGrab.grab(bbox=(left, top, left + width, top + height))

            if list(current_image.getdata()) == list(previous_image.getdata()):
                print("Reached to extreme")
                stop_event.set() 
                setup_scrolling.scroll_thread = None
                break
            previous_image = current_image 
        
        print(f"Scrolling {direction}...")  # Simulate scrolling action
          # Simulate delay between scroll actions
    print(f"Stopped scrolling {direction}.")

def start_scrolling(direction: str) -> None:
    """Start a new scroll thread."""
    setup_scrolling.stop_scroll_event.clear()
    setup_scrolling.scroll_thread = threading.Thread(target=start_gradual_scroll, args=(direction, setup_scrolling.stop_scroll_event))
    setup_scrolling.scroll_thread.start()

def stop_scrolling() -> None:
    """Stop the current scrolling thread."""
    setup_scrolling.stop_scroll_event.set()
    if setup_scrolling.scroll_thread is not None:
        setup_scrolling.scroll_thread.join()
        setup_scrolling.scroll_thread = None
    print("Scrolling has stopped.")


def scroll_to(direction:str)->None:
    active_window = gw.getActiveWindow()
    if active_window:
        # Bring the active window to the front
        active_window.activate()
        time.sleep(0.5)
        if direction=='top':
            pag.press('home') 
       
        elif direction=='bottom':
            pag.press('end') 
       
        elif direction=='right':
            pag.press('right', presses=9999) 
        
        elif direction=='left':
            pag.press('left', presses=9999) 
        
        else:
            print("Invalid Command")
        
        
#pygetwindow and implement
def simple_scroll(direction:str)->None:
    active_window = gw.getActiveWindow()
    if active_window:
        # Bring the active window to the front
        active_window.activate()
        time.sleep(0.5)
        if direction=='up':
            pag.press('up', presses=100) 
        elif direction=='down':
            pag.press('down', presses=100) 
        elif direction=='right':
            pag.press('right', presses=500) 
        elif direction=='left':
            pag.press('left', presses=500) 
        
        else:
            print("Invalid direction")
    

