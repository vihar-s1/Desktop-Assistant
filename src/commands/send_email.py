import re
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import dotenv_values

from infra import listen, load_json_config
from voice_interface import VoiceInterface

CONFIG_FILE = "mail_server.json"
SERVER = "server"
PORT = "port"
EMAIL_CONTACTS = "contacts"
SENDER = "username"
SMTP_PASS = "SMTP_PASSWORD"

ENV = dotenv_values(".env")


class SendEmail:

    @staticmethod
    def commandName() -> str:
        return SendEmail.__name__

    @staticmethod
    def validateQuery(query: str) -> bool:
        return "email" in query

    @staticmethod
    def executeQuery(query: str, vi: VoiceInterface) -> None:
        query = query.lower()

        data = load_json_config(CONFIG_FILE)

        server = data.get(SERVER)
        port = data.get(PORT)
        sender = data.get(SENDER)
        contacts = data.get(EMAIL_CONTACTS)

        if data.get("server") is None:
            vi.speak("Please setup email config file before sending mail.")
        else:
            vi.speak("who do you want to send email to?")
            receiver = None
            validEmail = False
            maxAttempts = 3
            while not validEmail and maxAttempts > 0:
                maxAttempts -= 1
                receiver = listen(vi).strip()

                if receiver in contacts.keys():
                    print(f"Receiver selected from contacts: {contacts.get(receiver)}")
                    receiver = contacts.get(receiver)
                    validEmail = True
                elif re.match(
                    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", receiver
                ):
                    validEmail = True
                else:
                    vi.speak("Valid Email not provided or contact does not exists")

            vi.speak("What would be the subject of the message? ")
            subject = listen(vi)

            vi.speak("What would be the body of the email?")
            body = None
            maxAttemptsForBody = 3
            while body is None and maxAttemptsForBody > 0:
                maxAttemptsForBody -= 1
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
    def __send_email(
        vi: VoiceInterface,
        server: str,
        port: str,
        fromEmail: str,
        toEmail: str,
        subject: str,
        body: str,
    ):
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

        context = ssl.create_default_context()
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = fromEmail
        msg["To"] = [toEmail]
        msg.set_content(body)
        server = smtplib.SMTP_SSL(server, port, context=context)
        server.login(fromEmail, ENV.get(SMTP_PASS))
        server.send_message(msg)
        server.quit()
        vi.speak(f"Email sent to {toEmail}")
