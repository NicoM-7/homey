import smtplib
from email.message import EmailMessage
import os

def send_email(to_email, subject, content):
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = to_email
    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_user, email_password)
        smtp.send_message(msg)