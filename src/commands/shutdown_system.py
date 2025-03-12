import subprocess

from voice_interface import VoiceInterface


class ShutdownSystem:

    @staticmethod
    def commandName():
        return ShutdownSystem.__name__

    @staticmethod
    def validateQuery(query: str) -> bool:
        return any(text in query for text in ["shutdown", "shut down"])

    @staticmethod
    def executeQuery(query: str, vi: VoiceInterface):
        subprocess.run(["shutdown", "-s", "/t", "1"])
