import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TEST_RECEIVER = "nehadhaked107@gmail.com"

msg = MIMEText("This is a test email from Flask.")
msg["Subject"] = "Test Email"
msg["From"] = EMAIL_SENDER
msg["To"] = TEST_RECEIVER

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, TEST_RECEIVER, msg.as_string())
    server.quit()
    print("✅ Test email sent successfully!")
except Exception as e:
    print(f"❌ Email Error: {e}")
