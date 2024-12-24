import os
from dotenv import load_dotenv

load_dotenv()

JIRA_API_URL = os.getenv('JIRA_API_URL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
TEMPO_API_URL = os.getenv('TEMPO_API_URL')
TEMPO_TOKEN = os.getenv('TEMPO_TOKEN')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
