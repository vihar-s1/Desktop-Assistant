import wikipedia

from voice_interface import VoiceInterface


class WikipediaSearch:
    """Searches wikipedia for the given query and returns fixed number of statements in response.
    Disambiguation Error due to multiple similar results is handled.
    Speaks the options in this case.
    """

    sentence_count = 3

    @staticmethod
    def commandName() -> str:
        return WikipediaSearch.__name__

    @staticmethod
    def validateQuery(query: str) -> bool:
        return "wikipedia" in query

    @staticmethod
    def executeQuery(query: str, vi: VoiceInterface) -> None:
        """
        Args:
            search_query (str): the query term to be searched in google
        """
        if not WikipediaSearch.validQuery(query):
            vi.speak("Invalid Wikipedia Search Query Found!!")
            return

        search_query = query.replace("wikipedia", "", 1).replace("search", "", 1)
        try:
            vi.speak("Searching Wikipedia...")
            results = wikipedia.summary(
                search_query, sentences=WikipediaSearch.sentence_count
            )

            vi.speak("According to wikipedia...")
            vi.speak(results)
        except wikipedia.DisambiguationError as de:
            vi.speak(f"\n{de.__class__.__name__}")
            options = str(de).split("\n")
            if len(options) < 7:
                for option in options:
                    vi.speak(option)
            else:
                for option in options[0:6]:
                    vi.speak(option)
                vi.speak("... and more")
