import os
from dotenv import load_dotenv
import requests

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(message: str):
    if not SLACK_WEBHOOK_URL:
        print("Slack webhook URL not configured.")
        return

    payload = {
        "text": message
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Slack alert sent successfully.")
    except requests.exceptions.RequestException as e:
        print("Failed to send Slack alert:", str(e))
