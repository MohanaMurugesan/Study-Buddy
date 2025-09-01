import smtplib
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText

load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_otp_mail(email:str,otp_code:str):
    subject = "Study Buddy OTP"
    body = f"Your OTP is {otp_code}"
    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    try:
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e :
        print(f"Failed to send otp email:{str(e)}")