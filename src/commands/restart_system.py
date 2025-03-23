import subprocess


class RestartSystem:

    @staticmethod
    def command_name():
        return RestartSystem.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return any(text in query for text in ["restart"])

    @staticmethod
    def execute_query(*_):
        subprocess.run(["shutdown", "/r", "/t", "1"], check=True)
