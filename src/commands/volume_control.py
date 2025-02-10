from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


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
