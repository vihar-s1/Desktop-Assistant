import re
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import dotenv_values

from infra import listen, load_json_config
from voice_interface import VoiceInterface

__CONFIG_FILE__ = "mail_server.json"
__SERVER__ = "server"
__PORT__ = "port"
__EMAIL_CONTACTS__ = "contacts"
__SENDER__ = "username"
__SMTP_PASS__ = "SMTP_PASSWORD"

__ENV__ = dotenv_values(".env")


class SendEmail:

    @staticmethod
    def command_name() -> str:
        return SendEmail.__name__

    @staticmethod
    def validate_query(query: str) -> bool:
        return "email" in query

    @staticmethod
    def execute_query(query: str, vi: VoiceInterface) -> None:
        query = query.lower()

        data = load_json_config(__CONFIG_FILE__)

        server = data.get(__SERVER__)
        port = data.get(__PORT__)
        sender = data.get(__SENDER__)
        contacts = data.get(__EMAIL_CONTACTS__)

        if data.get("server") is None:
            vi.speak("Please setup email config file before sending mail.")
        else:
            vi.speak("who do you want to send email to?")
            receiver = None
            valid_email = False
            max_attempts = 3
            while not valid_email and max_attempts > 0:
                max_attempts -= 1
                receiver = listen(vi).strip()

                if receiver in contacts.keys():
                    print(f"Receiver selected from contacts: {contacts.get(receiver)}")
                    receiver = contacts.get(receiver)
                    valid_email = True
                elif re.match(
                    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", receiver
                ):
                    valid_email = True
                else:
                    vi.speak("Valid Email not provided or contact does not exists")

            vi.speak("What would be the subject of the message? ")
            subject = listen(vi)

            vi.speak("What would be the body of the email?")
            body = None
            max_attempts_for_body = 3
            while body is None and max_attempts_for_body > 0:
                max_attempts_for_body -= 1
                body = listen(vi)

            print(
                f"Sender Address: {sender}\n"
                + f"Receiver address: {receiver}\n"
                + f"Subject: {subject}\n"
                + f"Body: {body}\n"
            )

            vi.speak("Do You Want to send this email?")
            response = None
            while response is None:
                response = listen(vi)
            if "yes" in response.lower() or "sure" in response.lower():
                vi.speak("Sending the email")
                SendEmail.__send_email(
                    vi, server, port, sender, receiver, subject, body
                )
            else:
                vi.speak("Request aborted by user")

    @staticmethod
    def __send_email(*args):
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

        vi, server, port, from_email, to_email, subject, body = args

        context = ssl.create_default_context()
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = [to_email]
        msg.set_content(body)
        server = smtplib.SMTP_SSL(server, port, context=context)
        server.login(from_email, __ENV__.get(__SMTP_PASS__))
        server.send_message(msg)
        server.quit()
        vi.speak(f"Email sent to {to_email}")
