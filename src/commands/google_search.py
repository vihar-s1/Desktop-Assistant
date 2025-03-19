import re

import googlesearch

from voice_interface import VoiceInterface


class GoogleSearch:

    @staticmethod
    def command_name() -> str:
        return GoogleSearch.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return re.search(r"search .* (in google)?", query)

    @staticmethod
    def execute_query(query: str, vi: VoiceInterface) -> None:
        search_query = re.findall(r"search (.*)", query.replace("in google", ""))[0]
        results = googlesearch.search(term=search_query)
        if not results:
            vi.speak("No Search Result Found!!")
        else:
            results = list(results)
            vi.speak("Found Following Results: ")
