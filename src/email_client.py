import abc
import html
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.domain import UnregisteredComment, Message, Email


class EmailClient(abc.ABC):

    @abc.abstractmethod
    def notify_new_comment(self, comment: UnregisteredComment):
        raise NotImplementedError

    @abc.abstractmethod
    def notify_new_message(self, comment: Message):
        raise NotImplementedError

    @abc.abstractmethod
    def notify_new_subscription(self, email: Email):
        raise NotImplementedError


class DisabledEmailClient(EmailClient):

    def notify_new_comment(self, comment: UnregisteredComment):
        print("notify_new_comment", comment)

    def notify_new_message(self, message: Message):
        print("notify_new_message", message)

    def notify_new_subscription(self, email: Email):
        print("notify_new_subscription", email)


class SMTPEmailClient(EmailClient):

    def notify_new_comment(self, comment: UnregisteredComment):
        message = MIMEMultipart()
        message["From"] = "an-amazing-buddy@petitapetit.io"
        message["To"] = "a@petitapetit.io"
        message["Subject"] = f"[{comment.post_slug}] {comment.author_name} a commenté"
        message["Reply-To"] = comment.author_email

        message.attach(MIMEText(html.unescape(comment.message), "plain"))

        try:
            with smtplib.SMTP("localhost", 25) as server:
                server.send_message(message)
        except Exception as e:
            print(f"Error sending email: {e}")

    def notify_new_message(self, comment: Message):
        message = MIMEMultipart()
        message["From"] = "an-amazing-buddy@petitapetit.io"
        message["To"] = "a@petitapetit.io"
        message["Subject"] = f"[petitapetit.io] {comment.author_name} viens de t'envoyer un message"
        message["Reply-To"] = comment.author_email

        message.attach(MIMEText(html.unescape(comment.message), "plain"))

        try:
            with smtplib.SMTP("localhost", 25) as server:
                server.send_message(message)
        except Exception as e:
            print(f"Error sending email: {e}")

    def notify_new_subscription(self, email: Email):
        print("notify_new_subscription: TODO")

