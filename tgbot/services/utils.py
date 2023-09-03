import asyncio
from email.message import EmailMessage

from aiosmtplib import SMTP


async def send_email(subject, body, sender, receiver, user, password):
    message = EmailMessage()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.set_content(body)

    smtp_client = SMTP(hostname='smtp.gmail.com', port=465, use_tls=True)
    async with smtp_client:
        await smtp_client.login(user, password)
        await smtp_client.send_message(message)
