import os, re
import googlesearch, wikipedia
from Extras import AppPath, WebPath, features
from VoiceInterface import VoiceInterface
from datetime import datetime

def clrscr():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")
        
        
def possibleAppsAndWebs(vi: VoiceInterface) -> None:
    vi.speak("Here is a list of all apps and websites I can open:")
    vi.speak("\n".join(AppPath.keys()))
    vi.speak("\n".join(WebPath.keys()))
    

def explainFeatures(vi: VoiceInterface) -> None:
    """Explains the features available

    Args:
        vi (VoiceInterface): The voice interface instance used to speak the text
    """
    vi.speak("Here's what I can do...\n")
    for feature in features:
        vi.speak(f"--> {feature}")
    

def runSearchQuery(vi: VoiceInterface, searchQuery: str) -> None:
    """Performs google seach based on some terms

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak
        searchQuery (str): the query term to be searched in google
    """
    if not isinstance(vi, VoiceInterface):
        raise ValueError(f"Arguement 'vi' should be of type {VoiceInterface}, found {type(vi)}")
    if not searchQuery:
        vi.speak("Invalid Google Search Query Found!!")
        return
    
    results = googlesearch.search(term=searchQuery)
    if not results: vi.speak("No Search Result Found!!")
    
    try:
        results = list(results)
        vi.speak("Found Following Results: ")
        for i in range(len(results)):
            print(i+1, ")", results[i])
    except Exception as eobj:
        print(eobj.__str__)
        

def wikipediaSearch(vi: VoiceInterface, searchQuery: str, sentenceCount:int=3) -> None:
    """Searches wikipedia for the given query and returns fixed number of statements in response.
    Disambiguation Error due to multiple similar results is handled. Speaks the options in this case.

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        searchQuery (str): The query term to search in wikipedia
        sentenceCount (int, optional): The number of sentences to speak in case of direct match. Defaults to 3.
    """
    try:
        vi.speak("Searching Wikipedia...")
        results = wikipedia.summary(searchQuery, sentences=sentenceCount)
        
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
        

def openApplicationWebsite(vi: VoiceInterface, searchQuery: str) -> None:
    """Attempts to raise the application or website by finding the accesspoint in the AppPath/WebPath dictionaries

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        searchQuery (str): The website or application name

    Raises:
        ValueError: Throws exception in case neither app nor web accesspoint is present.
    """
    vi.speak(f"Attempting to open {searchQuery}...")
    if searchQuery in AppPath.keys():
        try:  os.startfile(AppPath[searchQuery.strip()])
        except Exception as eobj:
            vi.speak(f"Error: {eobj}: Failed to open {searchQuery}")
        
    elif searchQuery in WebPath.keys():
        try:  os.startfile(WebPath[searchQuery.strip()])
        except Exception as eobj:
            vi.speak(f"Error: {eobj}: Failed to open {searchQuery}")
    
    else:
        raise ValueError(f"Missing Accesspoint for {searchQuery}")


def tellTime(vi: VoiceInterface) -> None:
    """Tells the time of the day with timezone

    Args:
        vi (VoiceInterface): Voice interface instance used to speak
    """
    if not isinstance(vi, VoiceInterface):
        raise ValueError(f"Arguement 'vi' should be of type {VoiceInterface}, found {type(vi)}")
    
    date_time = datetime.now()
    hour, minute, second = date_time.hour, date_time.minute, date_time.second
    tmz = date_time.tzname()
    
    vi.speak(f"Current time is {hour}:{minute}:{second} {tmz}")