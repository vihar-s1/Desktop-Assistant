import wmi


def brightness_control(value: int, relative: bool, toDecrease: bool):
    """
    Adjusts the brightness of the monitor.

    Args:
        value (int): The brightness level to set or adjust by. Should be between 0 and 100.
        relative (bool):    If True, the brightness change is relative to the current brightness.
                            If False, the brightness is set to the specified value.
        toDecrease (bool):  If True, decreases the brightness by the specified value.
                            If False, increases the brightness by the specified value. Only applicable when `relative` is True.

    Raises:
        RuntimeError: If there is an issue with accessing the brightness control methods.

    Returns:
        None
    """

    brightness_ctrl = wmi.WMI(namespace="root\\wmi")
    methods = brightness_ctrl.WmiMonitorBrightnessMethods()[0]

    if relative:
        current_brightness = brightness_ctrl.WmiMonitorBrightness()[0].CurrentBrightness
        set_brightnes = (
            current_brightness - int(value)
            if toDecrease
            else current_brightness + int(value)
        )
        methods.WmiSetBrightness(set_brightnes, 0)
    else:
        methods.WmiSetBrightness(value, 0)
