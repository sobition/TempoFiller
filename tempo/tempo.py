#!/usr/bin/env python3

import requests
import json
import argparse
from pathlib import Path
import base64

from config.settings import TEMPO_API_URL, TEMPO_TOKEN, JIRA_API_TOKEN, JIRA_EMAIL, ACCOUNT_ID, JIRA_API_URL

CACHE_FILE = Path("/tmp/tempo_accounts_cache.json")
WBSO_FIELD_ID = "customfield_11510"  # Replace with the actual custom field ID for WBSO Topic


auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
auth_header = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
authorization_header = f"Basic {auth_header}"

headers = {
    "Authorization": authorization_header,
    "Content-Type": "application/json"
}


def fetch_tempo_accounts():
    if CACHE_FILE.exists() and CACHE_FILE.stat().st_size > 0:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)

    url = f"{TEMPO_API_URL}/accounts"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    accounts = response.json().get("results", [])
    with open(CACHE_FILE, "w") as f:
        json.dump(accounts, f)
    return accounts

def find_account_key_by_id(accounts, account_id):
    return next((acc["key"] for acc in accounts if acc["id"] == account_id), None)

def fetch_issue(issue_key):
    url = f"{JIRA_API_URL}/{issue_key}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def extract_wbso_topic(issue_data):
    return issue_data["fields"].get(WBSO_FIELD_ID)

def report_time(account_key, issue_key, start_date, time_spent_hours, comment=None):
    url = f"{TEMPO_API_URL}/worklogs"
    headers = {"Authorization": f"Bearer {TEMPO_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "issueKey": issue_key,
        "timeSpentSeconds": int(float(time_spent_hours) * 3600),
        "startDate": start_date,
        "startTime": "09:00:00",
        "authorAccountId": ACCOUNT_ID,
        "attributes": [{"key": "_WBSOTopic_", "value": account_key}],
    }
    if comment:
        payload["description"] = comment

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Report time in Tempo.")
    parser.add_argument("issue_key", help="Issue key (e.g., IT-50)")
    parser.add_argument("start_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("time_spent", type=float, help="Time spent (in hours)")
    parser.add_argument("--comment", help="Optional comment for the worklog")

    args = parser.parse_args()

    issue_data = fetch_issue(args.issue_key)
    wbso_topic = extract_wbso_topic(issue_data)

    if not wbso_topic:
        print(f"No WBSO Topic found for issue {args.issue_key}.")
        exit(1)

    accounts = fetch_tempo_accounts()
    account_key = find_account_key_by_id(accounts, wbso_topic["id"])

    if not account_key:
        print(f"No Tempo Account Key found for WBSO Topic ID {wbso_topic['id']}. Time logging aborted.")
        exit(1)

    print(f"Reporting time for {args.issue_key} to Tempo account {account_key}.")
    report_time(account_key, args.issue_key, args.start_date, args.time_spent, args.comment)
    print("Time reported successfully!")
