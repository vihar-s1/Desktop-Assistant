import subprocess

from voice_interface import VoiceInterface


class RestartSystem:

    @staticmethod
    def commandName():
        return RestartSystem.__name__

    @staticmethod
    def validateQuery(query: str) -> bool:
        return any(text in query for text in ["restart"])

    @staticmethod
    def executeQuery(query: str, vi: VoiceInterface):
        subprocess.run(["shutdown", "/r", "/t", "1"])
