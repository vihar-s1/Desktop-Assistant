import re

import wmi

from voice_interface import VoiceInterface


class BrightnessControl:

    @staticmethod
    def command_name() -> str:
        return BrightnessControl.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return "brightness" in query

    @staticmethod
    def execute_query(query: str, vi: VoiceInterface) -> None:
        query = query.lower()

        value = re.findall(r"\b(100|[1-9]?[0-9])\b", query)
        if len(value) == 0 or str(value).isnumeric() == False:
            vi.speak("Please provide a valid brightness value between 0 and 100")
        else:
            value = min(max(0, int(value[0])), 100)
            if "set" in query:
                brightness_control(value, False, False)
            else:
                toDecrease = "decrease" in query or "reduce" in query
                relative = "by" in query
                brightness_control(value, relative, toDecrease)


def brightness_control(value: int, relative: bool, toDecrease: bool):
    """
    Adjusts the brightness of the monitor.

    Args:
        value (int): The brightness level to set or adjust by. Should be between 0 and 100.
        relative (bool):    If True, the brightness change is relative to the current brightness.
                            If False, the brightness is set to the specified value.
        toDecrease (bool):  If True, decreases the brightness by the specified value.
                            If False, increases the brightness by the specified value.
                            Only applicable when `relative` is True.

    Raises:
        RuntimeError: If there is an issue with accessing the brightness control methods.

    Returns:
        None
    """

    brightness_ctrl = wmi.WMI(namespace="root\\wmi")
    methods = brightness_ctrl.WmiMonitorBrightnessMethods()[0]

    if relative:
        current_brightness = brightness_ctrl.WmiMonitorBrightness()[0].CurrentBrightness
        set_brightness = (
            current_brightness - int(value)
            if toDecrease
            else current_brightness + int(value)
        )
        methods.WmiSetBrightness(set_brightness, 0)
    else:
        methods.WmiSetBrightness(value, 0)
