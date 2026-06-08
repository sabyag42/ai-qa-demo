import requests
import os
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

class JiraClient:

    def __init__(self):
        self.domain = os.getenv('JIRA_DOMAIN')
        self.email = os.getenv('JIRA_EMAIL')
        self.token = os.getenv('JIRA_API_TOKEN')
        self.base_url = f"https://{self.domain}/rest/api/3"

        # Build auth header
        credentials = f"{self.email}:{self.token}"
        encoded = b64encode(credentials.encode('utf-8')).decode('utf-8')
        self.headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json"
        }

    def get_issue(self, issue_key: str) -> dict:
        url = f"{self.base_url}/issue/{issue_key}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def extract_story_details(self, issue_key: str) -> dict:
        issue = self.get_issue(issue_key)

        # Extract summary
        summary = issue['fields']['summary']

        # Extract description — Jira uses Atlassian Document Format
        description_raw = issue['fields'].get('description', {})
        description_text = self._parse_description(description_raw)

        return {
            'key': issue_key,
            'summary': summary,
            'description': description_text
        }

    def _parse_description(self, description: dict) -> str:
        if not description:
            return "No description provided"

        lines = []
        content = description.get('content', [])

        for block in content:
            if block.get('type') == 'paragraph':
                for inline in block.get('content', []):
                    if inline.get('type') == 'text':
                        lines.append(inline.get('text', ''))
            elif block.get('type') == 'bulletList':
                for item in block.get('content', []):
                    for para in item.get('content', []):
                        for inline in para.get('content', []):
                            if inline.get('type') == 'text':
                                lines.append(f"- {inline.get('text', '')}")

        return '\n'.join(lines)


# Quick test
if __name__ == "__main__":
    client = JiraClient()
    story = client.extract_story_details('SCRUM-5')
    print(f"Key: {story['key']}")
    print(f"Summary: {story['summary']}")
    print(f"Description:\n{story['description']}")

    