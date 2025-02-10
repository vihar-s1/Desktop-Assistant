#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modify Settings
===============

This module contains functions to adjust system settings such as brightness and volume.

Functions:
    brightness_control(value: int, relative: bool, toDecrease: bool) -> None:
        Adjusts the brightness of the monitor.

    volume_control(value: int, relative: bool, toDecrease: bool) -> None:
        Adjusts the master volume of the system.
"""

import wmi
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


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
