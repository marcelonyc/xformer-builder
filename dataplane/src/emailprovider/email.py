import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailProvider:
    def __init__(self, config):
        self.smtp_host = config.smtp_host
        self.smtp_enabled = config.smtp_enabled
        self.smtp_port = config.smtp_port
        self.smtp_user = config.smtp_user
        self.smtp_password = config.smtp_password
        self.smtp_sender = config.smtp_sender

    def send_email(self, to, subject, body):
        if not self.smtp_enabled:
            return

        message = MIMEMultipart()
        message["From"] = self.smtp_sender
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            self.smtp_host, self.smtp_port, context=context
        ) as server:
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_sender, to, message.as_string())
