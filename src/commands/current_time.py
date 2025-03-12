from datetime import datetime

from voice_interface import VoiceInterface


class CurrentTime:
    """Tells the time of the day with timezone"""

    @staticmethod
    def commandName() -> str:
        return CurrentTime.__name__

    @staticmethod
    def validateQuery(query: str) -> bool:
        return any(text in query for text in ["the time", "time please"])

    @staticmethod
    def executeQuery(query: str, vi: VoiceInterface) -> None:
        """
        Args:
            vi (VoiceInterface): Voice interface instance used to speak
        """
        date_time = datetime.now()
        hour, minute, second = date_time.hour, date_time.minute, date_time.second
        tmz = date_time.tzname()

        vi.speak(f"Current time is {hour}:{minute}:{second} {tmz}")
