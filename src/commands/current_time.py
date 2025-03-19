from datetime import datetime

from voice_interface import VoiceInterface


class CurrentTime:

    @staticmethod
    def command_name() -> str:
        return CurrentTime.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return any(text in query for text in ["the time", "time please"])

    @staticmethod
    def execute_query(_: str, vi: VoiceInterface) -> None:
        date_time = datetime.now()
        hour, minute, second = date_time.hour, date_time.minute, date_time.second
        tmz = date_time.tzname()

        vi.speak(f"Current time is {hour}:{minute}:{second} {tmz}")
