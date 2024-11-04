import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import settings


class MailClient:

    def send_email_message(self, subject: str, text: str, to: str) -> None:
        msg = self.__build_message(subject, text, to)
        self.__send_email(msg)

    def __build_message(self, subject: str, text: str, to: str) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(text, "plain"))
        return msg

    def __send_email(self, msg: MIMEMultipart):
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context)
        server.login(settings.EMAIL_FROM, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
