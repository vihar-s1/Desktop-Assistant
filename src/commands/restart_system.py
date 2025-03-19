import subprocess

from voice_interface import VoiceInterface


class RestartSystem:

    @staticmethod
    def command_name():
        return RestartSystem.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return any(text in query for text in ["restart"])

    @staticmethod
    def execute_query(query: str, vi: VoiceInterface):
        subprocess.run(["shutdown", "/r", "/t", "1"])
