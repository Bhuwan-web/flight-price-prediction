"""Mail server config."""

import datetime
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType

from auth.config import CONFIG

mail_conf = ConnectionConfig(
    MAIL_USERNAME=CONFIG.mail_username,
    MAIL_PASSWORD=CONFIG.mail_password,
    MAIL_FROM=CONFIG.mail_sender,
    MAIL_PORT=CONFIG.mail_port,
    MAIL_SERVER=CONFIG.mail_server,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)

mail = FastMail(mail_conf)

async def send_verification_email(email: str, token: str) -> None:
    """Send user verification email."""
    try:
        url = CONFIG.root_url + "/mail/verify/" + token
        if CONFIG.mail_console:
            print("POST to " + url)
        else:
            message = MessageSchema(
                recipients=[email],
                subject="Verify Your Email - Flight Price Prediction App",
                body=f'''
                <html>
                  <head>
                    <style>
                      body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }}
                      .container {{ max-width: 600px; margin: 20px auto; background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }}
                      .header {{ text-align: center; font-size: 24px; font-weight: bold; color: #333; }}
                      .content {{ font-size: 16px; color: #555; line-height: 1.6; text-align: center; }}
                      .button {{ display: inline-block; padding: 12px 20px; margin: 20px 0; font-size: 16px; color: #ffffff !important; background: #007BFF; text-decoration: none; border-radius: 5px; border: none; }}
                      .button:hover {{ background: #0056b3; }}
                      .footer {{ font-size: 12px; color: #777; text-align: center; margin-top: 20px; }}
                      a.button {{ color: #ffffff !important; text-decoration: none; }}
                    </style>
                  </head>
                  <body>
                    <div class="container">
                      <div class="header">Flight Price Prediction App</div>
                      <p class="content">Welcome to our service! We just need to verify your email before you can start using your account.</p>
                      <p class="content">Click the button below to verify your email:</p>
                      <p style="text-align: center;"><a href="{url}" class="button" target="_blank">Verify Email</a></p>
                      <p class="content">If you did not sign up for this service, please ignore this email.</p>
                      <div class="footer">&copy; {datetime.datetime.now().year} Flight Price Prediction. All rights reserved.</div>
                    </div>
                  </body>
                </html>
                ''',
                subtype=MessageType.html,
            )
            await mail.send_message(message)
    except Exception as e:
        print(e)

async def send_password_reset_email(email: str, token: str) -> None:
    """Send password reset email."""
    # Change this later to public endpoint
    url = CONFIG.root_url + "/register/reset-password/" + token
    if CONFIG.mail_console:
        print("POST to " + url)
    else:
        message = MessageSchema(
            recipients=[email],
            subject="MyServer Password Reset",
            body=f"Click the link to reset your MyServer account password: {url}\nIf you did not request this, please ignore this email",
            subtype=MessageType.plain,
        )
        await mail.send_message(message)
