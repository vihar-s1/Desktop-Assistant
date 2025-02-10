#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Send Email
===============

This module contains functions to send emails using SMTP.

Functions:
    send_email(vi: VoiceInterface, toEmail: str, subject: str, body: str) -> None:
        Sends an email to the specified recipient.

        Args:
            vi (VoiceInterface): VoiceInterface instance used to speak.
            toEmail (str): The recipient's email address.
            subject (str): The subject of the email.
            body (str): The body content of the email.

        Raises:
            ValueError: If any required parameters are missing or invalid.
"""

import smtplib
import ssl
from email.message import EmailMessage

from dotenv import dotenv_values

from .utils import load_email_config
from .voice_interface import VoiceInterface

ENVIRONMENT_VARIABLES = dotenv_values(".env")


def send_email(vi: VoiceInterface, toEmail: str, subject: str, body: str):
    """
    Send an email to the specified recipient.

    Args:
        vi (VoiceInterface): VoiceInterface instance used to speak.
        toEmail (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Raises:
        ValueError: If any required parameters are missing or invalid.
    """

    data = load_email_config()
    CONTEXT = ssl.create_default_context()
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = data.get("username")
    msg["To"] = [toEmail]
    msg.set_content(body)
    server = smtplib.SMTP_SSL(data.get("server"), data.get("port"), context=CONTEXT)
    server.login(
        data.get("username"), ENVIRONMENT_VARIABLES.get("DESKTOP_ASSISTANT_SMTP_PWD")
    )
    server.send_message(msg)
    server.quit()
    vi.speak(f"Email sent to {toEmail}")
