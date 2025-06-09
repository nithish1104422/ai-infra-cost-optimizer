
from jira import JIRA
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

def create_jira_ticket(summary, description, issue_type="Task"):
    try:
        jira = JIRA(
            server=JIRA_SERVER,
            basic_auth=(JIRA_USER, JIRA_API_TOKEN)
        )

        issue = jira.create_issue(
            project=JIRA_PROJECT_KEY,
            summary=summary,
            description=description,
            issuetype={'name': issue_type}
        )

        print(f"Created Jira ticket: {issue.key}")
        return issue.key
    except Exception as e:
        print("Failed to create Jira ticket:", str(e))
        return None
