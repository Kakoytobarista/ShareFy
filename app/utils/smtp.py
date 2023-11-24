import os

from enums import SMTPCredsEnum
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

conf = ConnectionConfig(
    MAIL_USERNAME=SMTPCredsEnum.MAIL_USERNAME.value,
    MAIL_PASSWORD=SMTPCredsEnum.MAIL_PASSWORD.value,
    MAIL_FROM=SMTPCredsEnum.MAIL_FROM.value,
    MAIL_PORT=SMTPCredsEnum.MAIL_PORT.value,
    MAIL_SERVER=SMTPCredsEnum.MAIL_SERVER.value,
    MAIL_FROM_NAME=SMTPCredsEnum.MAIL_FROM_NAME.value,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER='./templates/email/'
)


async def send_email_async(subject: str, email_to: str, template_path: str, letter: bool = True) -> None:
    if letter:
        with open(template_path, "r") as file:
            html_content = file.read()
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=html_content,
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_email_background(background_tasks: BackgroundTasks,
                                subject: str,
                                email_to: str,
                                template_path: str,
                                letter: bool = True) -> None:
    if letter:
        with open(template_path, "r") as file:
            html_content = file.read()
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message, template_name=template_path)
