import subprocess


class ShutdownSystem:

    @staticmethod
    def command_name():
        return ShutdownSystem.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return any(text in query for text in ["shutdown", "shut down"])

    @staticmethod
    def execute_query(*_):
        subprocess.run(["shutdown", "-s", "/t", "1"], check=True)
