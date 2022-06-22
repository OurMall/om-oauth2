from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core import settings

email_template = """
    <div style="margin:0;background-color:#fff;padding:0;-webkit-text-size-adjust:none;text-size-adjust:none">
        <table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation"
            style="mso-table-lspace:0;mso-table-rspace:0;background-color:#fff">
            <tbody>
                <tr>
                    <td>
                        <table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0"
                            role="presentation" style="mso-table-lspace:0;mso-table-rspace:0">
                            <tbody>
                                <tr>
                                    <td>
                                        <table class="row-content stack" align="center" border="0" cellpadding="0"
                                            cellspacing="0" role="presentation"
                                            style="mso-table-lspace:0;mso-table-rspace:0;color:#000;width:500px"
                                            width="500">
                                            <tbody>
                                                <tr>
                                                    <td class="column column-1" width="100%"
                                                        style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;vertical-align:top;padding-top:5px;padding-bottom:5px;border-top:0;border-right:0;border-bottom:0;border-left:0">
                                                        <table class="image_block" width="100%" border="0" cellpadding="0"
                                                            cellspacing="0" role="presentation"
                                                            style="mso-table-lspace:0;mso-table-rspace:0">
                                                            <tr>
                                                                <td style="width:100%;padding-right:0;padding-left:0">
                                                                    <div align="center" style="line-height:10px">
                                                                        <img src="https://d15k2d11r6t6rl.cloudfront.net/public/users/BeeFree/beefree-p9gukl7wi09/editor_images/om-logo-6.png"
                                                                            style="display:block;height:auto;border:0;width:200px;max-width:100%"
                                                                            width="200">
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        {0}
                        <table class="row row-7" align="center" width="100%" border="0" cellpadding="0" cellspacing="0"
                            role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#fff">
                            <tbody>
                                <tr>
                                    <td>
                                        <table class="row-content stack" align="center" border="0" cellpadding="0"
                                            cellspacing="0" role="presentation"
                                            style="mso-table-lspace:0;mso-table-rspace:0;background-color:#f6f6f6;color:#000;width:500px"
                                            width="500">
                                            <tbody>
                                                <tr>
                                                    <td class="column column-1" width="100%"
                                                        style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;vertical-align:top;padding-top:5px;padding-bottom:5px;border-top:0;border-right:0;border-bottom:0;border-left:0">
                                                        <table class="html_block" width="100%" border="0" cellpadding="0"
                                                            cellspacing="0" role="presentation"
                                                            style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;word-wrap:break-word">
                                                            <tr>
                                                                <td>
                                                                    <div style="font-family:Arial,Helvetica Neue,Helvetica,sans-serif;text-align:center;background-color: #fff;"
                                                                        align="center">
                                                                        <button
                                                                            style="background-color: #005fc5; color:#fff; margin-top: 15px;border: none; border-radius: 15px;height: 40px; font-weight: 700; ">
                                                                            VERIFY EMAIL
                                                                        </button>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
"""

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
            email_format = MIMEText(email_template.format(kwds["message"]), kwds["format"])
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