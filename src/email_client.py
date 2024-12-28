import abc
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.domain import UnregisteredComment


class EmailClient(abc.ABC):

    @abc.abstractmethod
    def notify_new_comment(self, comment: UnregisteredComment):
        raise NotImplementedError


class DisabledEmailClient(EmailClient):

    def notify_new_comment(self, comment: UnregisteredComment):
        pass


class SMTPEmailClient(EmailClient):
    def notify_new_comment(self, comment: UnregisteredComment):
        # Create the email message
        message = MIMEMultipart()
        message['From'] = "comments@petitapetit.io"
        message['To'] = "a@petitapetit.io"
        message['Subject'] = f"[{comment.post_slug}] {comment.author_name} a commenté"
        message['Reply-To'] = comment.author_email

        message.attach(MIMEText(comment.message, 'plain'))

        try:
            with smtplib.SMTP('localhost', 25) as server:
                server.send_message(message)
        except Exception as e:
            print(f"Error sending email: {e}")
