#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utils
===============

This module contains utility functions for the desktop assistant.

Functions:
    load_email_config() -> dict:
        Loads the email configuration from a JSON file.

        Returns:
            dict: The email configuration data.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config", "email_config.json")


def load_email_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
