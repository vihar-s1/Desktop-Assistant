import feedparser

from voice_interface import VoiceInterface


class FetchNews:
    """
    Fetches and reads out the top 5 headlines from the Google News RSS feed.

    This function fetches news headlines from the Google News RSS feed (specific to India in English).
    It then reads out the top 5 headlines using the provided VoiceInterface instance. If the feed fetch is successful,
    it reads the headlines one by one. If the fetch fails, it informs the user that the news couldn't be fetched.

    Raises:
        requests.exceptions.RequestException: If there is an issue while fetching the RSS feed.
        AttributeError: If the feed does not contain expected attributes or entries.
    """

    # Maximum number of news headlines to fetch when news function is called
    MAX_FETCHED_HEADLINES = 10
    FEED_URL = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"

    @staticmethod
    def commandName() -> str:
        return FetchNews.__name__

    @staticmethod
    def validateQuery(query: str) -> bool:
        return "news" in query

    @staticmethod
    def executeQuery(query: str, vi: VoiceInterface) -> None:
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
