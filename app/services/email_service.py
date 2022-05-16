from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core import settings

class EmailService:
    
    def __init__(self) -> None:
        self._client = SMTP()
    
    def __call__(self, **kwds: dict[str, object]) -> object:
        if(not isinstance(self._client, SMTP)):
            self._client = SMTP(**kwds)
        pass
    
    async def _start_connection(self) -> None:
        await self._client.connect(
            hostname=settings.SMTP_HOSTNAME,
            port=settings.SMTP_PORT,
            timeout=5000
        )
        await self._client.starttls()
        await self._client.login(
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD
        )
    
    async def send_email(
        self, 
        to: list[str] | str, 
        subject: str | None, 
        **kwds: dict[str, object]
    ) -> None:
        """Method for send emails to users

        Args:
            to (list[str] | str): User or users list for send the email.
            subject (str | None): Email title

        Raises:
            e: _description_
        """
        await self._start_connection()
        if(isinstance(to, str)):
            to = [to]
        for email in to:
            mime = MIMEMultipart()
            mime['From'] = settings.SMTP_USERNAME
            mime['Subject'] = subject if subject is not None else "No-reply"
            mime['To'] = email
            email_format = MIMEText(kwds["message"], kwds["format"])
            mime.attach(email_format)
            try:
                await self._client.sendmail(settings.SMTP_USERNAME, email, mime.as_string())
            except Exception as e:
                #pass
                raise e
        await self._close_connection()
    
    async def _close_connection(self) -> None:
        await self._client.quit()

email_client = EmailService()