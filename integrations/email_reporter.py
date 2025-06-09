import boto3
from botocore.exceptions import ClientError
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SENDER = os.getenv("EMAIL_SENDER")
RECIPIENT = os.getenv("EMAIL_RECIPIENT")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def send_email(subject, html_content):
    client = boto3.client('ses', region_name=AWS_REGION)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    part = MIMEText(html_content, 'html')
    msg.attach(part)

    try:
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[RECIPIENT],
            RawMessage={'Data': msg.as_string()}
        )
        print("Email sent! Message ID:", response['MessageId'])
    except ClientError as e:
        print("Error sending email:", e.response['Error']['Message'])
