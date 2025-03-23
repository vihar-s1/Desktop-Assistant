import feedparser

from voice_interface import VoiceInterface


class FetchNews:
    # Maximum number of news headlines to fetch when news function is called
    MAX_FETCHED_HEADLINES = 10
    FEED_URL = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"

    @staticmethod
    def command_name() -> str:
        return FetchNews.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return "news" in query

    @staticmethod
    def execute_query(_: str, vi: VoiceInterface) -> None:
        vi.speak("Fetching news from servers.")
        feed = feedparser.parse(FetchNews.FEED_URL)
        if feed.status == 200:
            headlines_list = []
            for entry in feed.entries[: FetchNews.MAX_FETCHED_HEADLINES]:
                headlines_list.append((entry.title).split(" -")[0])
            vi.speak("Here are some recent news headlines.")
            for headline in headlines_list:
                vi.speak(headline)
        else:
            vi.speak("Failed to fetch the news.")
