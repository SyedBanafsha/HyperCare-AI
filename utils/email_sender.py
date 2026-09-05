import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

print("EMAIL:", repr(EMAIL_ADDRESS))
print("PASSWORD LENGTH:", len(EMAIL_PASSWORD) if EMAIL_PASSWORD else 0)

def send_prescription_email(
    receiver_email,
    patient_name,
    pdf_path
):

    message = EmailMessage()

    message["Subject"] = "HyperCare AI - Prescription"

    message["From"] = EMAIL_ADDRESS

    message["To"] = receiver_email

    message.set_content(
        f"""
Dear {patient_name},

Please find your prescription attached.

Thank you for choosing HyperCare AI Hospital.

Regards,
HyperCare AI Hospital
"""
    )

    with open(pdf_path, "rb") as file:
        file_data = file.read()

    message.add_attachment(
        file_data,
        maintype="application",
        subtype="pdf",
        filename=pdf_path
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(message)
        