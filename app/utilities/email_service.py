import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from .s3 import download_file_from_s3
import os


SENDER = "leadlegalco@gmail.com"
PASSWORD = "vvmk bfok dlax vyet"

def send_email(subject, body, recipient_email, resume_url=None):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = recipient_email

    # Attach the body with the text part
    msg.attach(MIMEText(body, 'plain'))

    # Open the file to be sent
    if resume_url:
        download_file_from_s3(resume_url, 'resume.pdf')
        if os.path.exists('resume.pdf'):
            with open('resume.pdf', "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)  # Encode file in base64 to send by email

                part.add_header(
                    'Content-Disposition',
                    f"attachment; filename= {'resume.pdf'}",
                )

                # Attach the file to the message
                msg.attach(part)
            os.remove('resume.pdf')

    # Using SMTP server to send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(SENDER, PASSWORD)
        smtp_server.send_message(msg)  # Using send_message instead of sendmail for MIME messages

