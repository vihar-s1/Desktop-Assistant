#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Infra
===============

This module contains implementations for various support functions and features of the Assistant.

"""

import os
import sys


def __is_windows() -> bool:
    """Returns True if the operating system is Windows"""
    return sys.platform in ["win32", "cygwin"]


def __is_darwin() -> bool:
    """Returns True if the operating system is Darwin"""
    return sys.platform in ["darwin", "ios"]


def __is_posix() -> bool:
    """Returns True if the operating system is POSIX"""
    return sys.platform in ["aix", "android", "emscripten", "linux", "darwin", "wasi"]


def __system_os() -> str:
    """Returns the name of the operating system"""
    return sys.platform


def clear_screen() -> None:
    """Clears the screen based on the operating system"""
    if __is_windows():
        os.system("cls")
    else:
        os.system("clear")
