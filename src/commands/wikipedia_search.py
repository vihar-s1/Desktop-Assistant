import wikipedia

from voice_interface import VoiceInterface


class WikipediaSearch:

    sentence_count = 3

    @staticmethod
    def command_name() -> str:
        return WikipediaSearch.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return "wikipedia" in query

    @staticmethod
    def execute_query(query: str, vi: VoiceInterface) -> None:
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
