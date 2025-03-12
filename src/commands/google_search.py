import re

import googlesearch

from voice_interface import VoiceInterface


class GoogleSearch:
    """Performs google search based on some terms"""

    @staticmethod
    def commandName() -> str:
        return GoogleSearch.__name__

    @staticmethod
    def validateQuery(query: str) -> bool:
        return re.search(r"search .* (in google)?", query)

    @staticmethod
    def executeQuery(query: str, vi: VoiceInterface) -> None:
        """
        Args:
            search_query (str): the query term to be searched in google
        """
        if not GoogleSearch.validQuery(query):
            vi.speak("Invalid Google Search Query Found!!")
            return

        search_query = re.findall(r"search (.*)", query.replace("in google", ""))[0]
        results = googlesearch.search(term=search_query)
        if not results:
            vi.speak("No Search Result Found!!")
        else:
            results = list(results)
            vi.speak("Found Following Results: ")
