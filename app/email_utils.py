import logging
from typing import Dict, Any
import mailtrap as mt
from app.config import settings, MailBody

logger = logging.getLogger(__name__)


class EmailError(Exception):
    """Exception raised for errors in the email sending process."""
    pass


def send_mail(data: Dict[str, Any]) -> None:
    """
    Send an email using the Mailtrap Python SDK.

    Args:
        data: Dictionary containing email details (to, subject, body)

    Raises:
        EmailError: If there's an error sending the email
    """
    try:
        msg = MailBody(**data)
        
        mail = mt.Mail(
            sender=mt.Address(email="hello@demomailtrap.co",
                              name="Meeting Victor"),
            to=[mt.Address(email="victorojo007@gmail.com")],
            subject=data["subject"],
            text=data["body"],
            category="Profile Messages",
        )

        client = mt.MailtrapClient(token=settings.MAILTRAP_API_TOKEN)
        response = client.send(mail)

        logger.info(f"Email sent successfully to {msg.to} - response: {response}")
    except Exception as e:
        logger.error(f"Unexpected error sending email: {str(e)}")
        raise EmailError(f"Unexpected error sending email: {str(e)}")