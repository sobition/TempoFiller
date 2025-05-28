<div style="display: flex; align-items: center; gap: 12px;" dir="auto">
  <a target="_blank" rel="noopener noreferrer" href="https://private-user-images.githubusercontent.com/33763156/448293130-07ab4b47-cfb8-4237-8055-783a5326f710.png?...">
    <img src="https://private-user-images.githubusercontent.com/33763156/448293130-07ab4b47-cfb8-4237-8055-783a5326f710.png?..." alt="Tempo Filler Logo" width="80" style="max-width: 100%;" />
  </a>
  <h1 style="margin: 0;">Tempo Filler Script</h1>
</div>


This script allows you to log work hours to Jira issues using the Tempo API. It supports fetching account details and reporting time directly from the terminal.

---

## Prerequisites

1. **Python Environment**: Ensure you have Python 3.7+ installed and a virtual environment set up.
2. **API Tokens and Credentials**:
   - **Jira API Token**: Generate from [Jira API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens).
   - **Tempo Token**: Generate from [Tempo API Configuration](https://{domain}.atlassian.net/plugins/servlet/ac/io.tempo.jira/tempo-app#!/configuration/api-integration).
   - **Account ID**: Retrieve from [Account Info](https://{domain}.atlassian.net/rest/api/3/myself).

---

## Setup

1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root of the project and populate it with the required environment variables:
   ```env
   JIRA_API_URL=https://{your-domain}.atlassian.net/rest/api/2/issue
   TEMPO_API_URL=https://api.tempo.io/core/3
   JIRA_API_TOKEN=your_jira_api_token
   TEMPO_TOKEN=your_tempo_token
   ACCOUNT_ID=your_account_id
   JIRA_EMAIL=your_email@example.com
   ```

## Usage

Run the script using the following command:

```bash
    python -m tempo.tempo ISSUE_KEY START_DATE TIME_SPENT [COMMENT]
```

### Parameters

1. **ISSUE_KEY**: The Jira issue key (e.g., ABC-123).
2. **START_DATE**: The date when the work was started (e.g., 2021-12-31).
3. **TIME_SPENT**: The time spent on the issue (e.g., 1h 30m).
4. **COMMENT** (Optional): A comment to add to the work log.

Example:

```bash
    python -m tempo.tempo ABC-123 2021-12-31 1.5 "Worked on the issue"
```

### How it works

1. The script fetches the Tempo account details from the API.
2. It identifies the correct account key for the Jira issue based on the WBSO Topic.(Netherlands specific)
3. It submits a work log to the Tempo API with the provided parameters.

### Notes

- Ensure your API tokens and credentials are kept secure.
- Update the domain placeholders ({domain}) in the token generation and account ID retrieval links to match your Jira instance.
