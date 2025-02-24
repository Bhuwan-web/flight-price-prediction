"""Mail server config."""

import datetime
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType

from auth.config import CONFIG
from auth.models.flight_record import FlightBookingDetails

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
    url = "http://localhost:5173/reset-password?token=" + token
    try:
        message = MessageSchema(
            recipients=[email],
            subject="MyServer Password Reset",
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
                  <div class="header">MyServer Password Reset</div>
                  <p class="content">You requested a password reset for your MyServer account. To reset your password, click the button below:</p>
                  <p style="text-align: center;"><a href="{url}" class="button" target="_blank">Reset Password</a></p>
                  <p class="content">If you did not request this, please ignore this email.</p>
                  <div class="footer">&copy; {datetime.datetime.now().year} MyServer. All rights reserved.</div>
                </div>
              </body>
            </html>
            ''',
            subtype=MessageType.html,
        )
        await mail.send_message(message)
    except Exception as e:
        print(e)
    

async def send_booking_email(flight_record: FlightBookingDetails) -> None:
    # Format the departure and arrival times for better readability
    departure_time = flight_record.departure_time.strftime("%Y-%m-%d %H:%M")
    arrival_time = flight_record.arrival_time.strftime("%Y-%m-%d %H:%M")

    # Calculate the total price based on quantity
    total_price = flight_record.predicted_price * flight_record.quantity

    # Create the HTML email body
    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flight Booking Confirmation</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f9f9f9;
                padding: 20px;
            }}
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #007BFF;
            }}
            .details {{
                margin-top: 20px;
            }}
            .details p {{
                margin: 10px 0;
            }}
            .total-price {{
                font-size: 1.2em;
                font-weight: bold;
                color: #28a745;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 0.9em;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <h1>Flight Booking Confirmation</h1>
            <p>Dear {flight_record.user_name},</p>
            <p>Your flight has been successfully booked! Below are the details of your booking:</p>

            <div class="details">
                <p><strong>Booking ID:</strong> {flight_record.booking_id}</p>
                <p><strong>Airline:</strong> {flight_record.airline}</p>
                <p><strong>Origin:</strong> {flight_record.origin}</p>
                <p><strong>Destination:</strong> {flight_record.destination}</p>
                <p><strong>Departure Time:</strong> {departure_time}</p>
                <p><strong>Arrival Time:</strong> {arrival_time}</p>
                <p><strong>Transit Count:</strong> {flight_record.transit_count}</p>
                <p><strong>Predicted Price per Ticket:</strong> ₹{flight_record.predicted_price:.2f}</p>
                <p><strong>Quantity:</strong> {flight_record.quantity}</p>
                <p class="total-price"><strong>Total Price:</strong> ₹{total_price:.2f}</p>
            </div>

            <p>If you did not book this flight, please contact us immediately at <a href="mailto:support@flightpriceprediction.com">support@flightpriceprediction.com</a>.</p>

            <div class="footer">
                <p>Thank you for using the Flight Price Prediction App!</p>
                <p>This is an automated email. Please do not reply directly to this message.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Create the email message
    message = MessageSchema(
        recipients=[flight_record.email],
        subject="Flight Booked - Flight Price Prediction App",
        body=email_body,
        subtype=MessageType.html,  # Use HTML for rich formatting
    )

    # Send the email
    await mail.send_message(message)

async def send_cancellation_email(flight_record: FlightBookingDetails) -> None:
    # Format the departure and arrival times for better readability
    departure_time = flight_record.departure_time.strftime("%Y-%m-%d %H:%M")
    arrival_time = flight_record.arrival_time.strftime("%Y-%m-%d %H:%M")

    # Calculate the total price based on quantity
    total_price = flight_record.predicted_price * flight_record.quantity

    # Create the HTML email body
    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flight Cancellation Confirmation</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f9f9f9;
                padding: 20px;
            }}
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #dc3545; /* Red color for cancellation */
            }}
            .details {{
                margin-top: 20px;
            }}
            .details p {{
                margin: 10px 0;
            }}
            .total-price {{
                font-size: 1.2em;
                font-weight: bold;
                color: #28a745;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 0.9em;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <h1>Flight Cancellation Confirmation</h1>
            <p>Dear {flight_record.user_name},</p>
            <p>We confirm that your flight has been successfully cancelled. Below are the details of the cancelled booking:</p>

            <div class="details">
                <p><strong>Flight ID:</strong> {flight_record.flight_id}</p>
                <p><strong>Airline:</strong> {flight_record.airline}</p>
                <p><strong>Origin:</strong> {flight_record.origin}</p>
                <p><strong>Destination:</strong> {flight_record.destination}</p>
                <p><strong>Departure Time:</strong> {departure_time}</p>
                <p><strong>Arrival Time:</strong> {arrival_time}</p>
                <p><strong>Transit Count:</strong> {flight_record.transit_count}</p>
                <p><strong>Predicted Price per Ticket:</strong> ₹{flight_record.predicted_price:.2f}</p>
                <p><strong>Quantity:</strong> {flight_record.quantity}</p>
                <p class="total-price"><strong>Total Price Refunded:</strong> ₹{total_price:.2f}</p>
            </div>

            <p>If you did not request this cancellation, please contact us immediately at <a href="mailto:support@flightpriceprediction.com">support@flightpriceprediction.com</a>.</p>

            <div class="footer">
                <p>Thank you for using the Flight Price Prediction App!</p>
                <p>This is an automated email. Please do not reply directly to this message.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Create the email message
    message = MessageSchema(
        recipients=[flight_record.email],
        subject="Flight Cancellation - Flight Price Prediction App",
        body=email_body,
        subtype=MessageType.html,  # Use HTML for rich formatting
    )

    # Send the email
    await mail.send_message(message)