"""
This module defines the `ShutdownSystem` class, which provides functionality to handle system shutdown commands. 
It includes methods to validate user queries for shutdown-related keywords and execute the shutdown command.
Classes:
    ShutdownSystem: A class to validate and execute system shutdown commands.
"""

import subprocess

from voice_interface import VoiceInterface


class ShutdownSystem:

    @staticmethod
    def command_name():
        return ShutdownSystem.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return any(text in query for text in ["shutdown", "shut down"])

    @staticmethod
    def execute_query(query: str, vi: VoiceInterface):
        subprocess.run(["shutdown", "-s", "/t", "1"])
