import re

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from voice_interface import VoiceInterface


class VolumeControl:

    @staticmethod
    def commandName() -> str:
        return VolumeControl.__name__

    @staticmethod
    def validateQuery(query: str) -> bool:
        return any(text in query for text in ["volume", "sound"])

    @staticmethod
    def executeQuery(query: str, vi: VoiceInterface) -> None:
        query = query.lower()
        value = re.findall(r"\b(100|[1-9]?[0-9])\b", query)

        if len(value) == 0 or str(value).isnumeric() == False:
            vi.speak("Please provide a value or input is out of range")
        else:
            value = min(max(0, int(value[0])), 100)
            if "set" in query:
                volume_control(value, False, False)
            else:
                toDecrease = "decrease" in query or "reduce" in query
                relative = "by" in query
                volume_control(value, relative, toDecrease)


def volume_control(value: int, relative: bool, toDecrease: bool):
    """
    Adjusts the master volume of the system.

    Args:
        value (int): The volume level to set or adjust by. Should be between 0 and 100.
        relative (bool): If True, the volume change is relative to the current volume.
                         If False, the volume is set to the specified value.
        toDecrease (bool): If True, decreases the volume by the specified value.
                           If False, increases the volume by the specified value. Only applicable when `relative` is True.

    Raises:
        RuntimeError: If there is an issue with accessing the audio endpoint.

    Returns:
        None
    """

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    if relative:
        current_volume = volume.GetMasterVolumeLevelScalar() * 100
        set_volume = (
            current_volume - int(value) if toDecrease else current_volume + int(value)
        )
        print(set_volume)
        volume.SetMasterVolumeLevelScalar(min(max(0, set_volume), 100) / 100, None)
    else:
        volume.SetMasterVolumeLevelScalar(min(max(0, value), 100) / 100, None)
