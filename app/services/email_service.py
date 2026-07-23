import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings
from loguru import logger


async def send_email(to_email: str, subject: str, html_content: str):
    if not all([
        settings.SMTP_HOST,
        settings.SMTP_USER,
        settings.SMTP_PASSWORD,
        settings.SMTP_FROM_EMAIL
    ]):
        logger.warning("SMTP settings not configured, skipping email")
        return

    def _send():
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

    try:
        await asyncio.to_thread(_send)
        logger.info(f"Email sent to {to_email}: {subject}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")


def create_contact_email_html(data, ai) -> str:
    return f"""
    <h2>Новое обращение с сайта</h2>
    <p><strong>Имя:</strong> {data.name}</p>
    <p><strong>Телефон:</strong> {data.phone}</p>
    <p><strong>Email:</strong> {data.email}</p>
    <p><strong>Комментарий:</strong> {data.comment}</p>
    <hr/>
    <p><strong>Тональность:</strong> {ai.get("sentiment", "unknown")}</p>
    <p><strong>Категория:</strong> {ai.get("category", "general")}</p>
    <p><strong>Автоответ:</strong> {ai.get("auto_reply", "")}</p>
    """


def create_user_reply_html(data, ai) -> str:
    return f"""
    <h2>Спасибо за ваше обращение</h2>
    <p>Уважаемый(ая) {data.name},</p>
    <p>Мы получили ваше сообщение и скоро свяжемся с вами.</p>
    <p><strong>Ваш комментарий:</strong> {data.comment}</p>
    <p><strong>Наш ответ:</strong> {ai.get("auto_reply", "Спасибо за обращение!")}</p>
    <p>С уважением,<br/>Команда поддержки</p>
    """
