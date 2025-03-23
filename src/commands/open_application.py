import re
import subprocess
from subprocess import CalledProcessError, TimeoutExpired

from AppOpener import open as open_app

import infra
from voice_interface import VoiceInterface


class OpenApplication:

    @staticmethod
    def command_name() -> str:
        return OpenApplication.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return re.search("open .*", query)

    @staticmethod
    def execute_query(query: str, vi: VoiceInterface) -> None:
        application = re.findall(r"open (.*)", query)
        if len(application) == 0:
            vi.speak("Which Application Should I Open ?")
            return
        application = application[0]
        try:
            open_application_website(vi, application)
        except ValueError as ve:
            print(
                f"Error occurred while opening {application}: {ve.__class__.__name__}: {ve}"
            )
            vi.speak(f"Failed to open {application}. Please try again.")


def open_application_website(vi: VoiceInterface, search_query: str) -> None:
    """
    open the application/website using a matching path from AppPath/WebPath dictionaries.

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The website or application name

    Raises:
        ValueError: Throws exception in case neither app nor web access-point is present.
    """
    vi.speak(f"Attempting to open {search_query}...")

    search_query = search_query.strip().lower()

    # use appopener to open the application only if os is windows
    if infra.is_windows():
        __open_application_website_windows(vi, search_query)
    if infra.is_darwin():
        __open_application_website_darwin(vi, search_query)
    elif infra.is_posix():
        __open_application_website_posix(vi, search_query)
    else:
        raise ValueError(f"Unsupported OS: {infra.system_os()}")


def __open_application_website_windows(vi: VoiceInterface, search_query: str) -> None:
    """handle the opening of application/website for Windows OS

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The website or application name

    Raises:
        ValueError: Throws exception in case neither app nor web access-point is present.
    """
    try:
        open_app(search_query, match_closest=True)  # attempt to open as application
    except Exception as error:
        vi.speak(f"Error: {error}: Failed to open {search_query}")


def __open_application_website_darwin(vi: VoiceInterface, search_query: str) -> None:
    """handle the opening of application/website for Darwin OS

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The website or application name

    Raises:
        ValueError: Throws exception in case neither app nor web access-point is present.
    """
    try:
        subprocess.run(
            ["open", "-a", search_query], capture_output=True, check=True
        )  # attempt to open as application
    except CalledProcessError:
        try:
            subprocess.run(
                ["open", search_query], capture_output=True, check=True
            )  # attempt to open as website
        except CalledProcessError as error:
            return_code = error.returncode
            stdout_text = error.stdout.decode("utf-8")
            stderr_text = error.stderr.decode("utf-8")
            vi.speak(
                f"Error: {error}: Failed to open {search_query}: error code {return_code}"
            )
            if stdout_text:
                print("stdout:", stdout_text)
            if stderr_text:
                print("stderr:", stderr_text)
        except TimeoutExpired as error:
            vi.speak(f"Error: {error}: Call to open {search_query} timed out.")

    except TimeoutExpired as error:
        vi.speak(f"Error: {error}: Call to open {search_query} timed out.")


def __open_application_website_posix(vi: VoiceInterface, search_query: str) -> None:
    """handle the opening of application/website for POSIX OS

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        search_query (str): The website or application name

    Raises:
        ValueError: Throws exception in case neither app nor web access-point is present.
    """
    try:
        subprocess.run(
            ["xdg-open", search_query], capture_output=True, check=True
        )  # attempt to open website/application
    except CalledProcessError as error:
        vi.speak(
            f"Error: {error}: Failed to open {search_query}: error code {error.returncode}"
        )
        stdout_text = error.stdout.decode("utf-8")
        stderr_text = error.stderr.decode("utf-8")
        if stdout_text:
            print("stdout:", stdout_text)
        if stderr_text:
            print("stderr:", stderr_text)

    except TimeoutExpired as error:
        vi.speak(f"Error: {error}: Call to open {search_query} timed out.")
