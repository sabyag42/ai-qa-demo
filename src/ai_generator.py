import os
from openai import OpenAI
from dotenv import load_dotenv
from src.jira_client import JiraClient

load_dotenv()

class AIGenerator:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o-mini"

    def generate_test_cases(self, story: dict) -> str:
        prompt = f"""
You are a senior QA engineer. Based on the following Jira user story, 
generate structured test cases.

Story Key: {story['key']}
Summary: {story['summary']}
Description: {story['description']}

Generate test cases in this exact format:
TC1: [Test case title]
Steps:
1. [Step 1]
2. [Step 2]
Expected: [Expected result]

TC2: [Test case title]
Steps:
1. [Step 1]
Expected: [Expected result]

Generate at least 6 test cases covering:
- Happy path login
- Invalid credentials
- Empty fields
- Locked out user
- Password only (no username)
- Username only (no password)
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior QA engineer who writes clear, structured test cases."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    def generate_playwright_script(self, test_cases: str, story: dict) -> str:
        prompt = f"""
You are a senior automation engineer. Convert these test cases into 
a working Playwright Python script using pytest.

Story: {story['summary']}

Test Cases:
{test_cases}

Requirements:
- Use playwright with pytest
- Target URL: https://www.saucedemo.com
- Use page object pattern
- Include proper assertions
- Add @pytest.mark.smoke for happy path tests
- Add @pytest.mark.regression for all tests
- Return ONLY the Python code, no explanations
- Saucedemo error messages always start with "Epic sadface: " prefix
- Make sure to add a few more negative test cases as well
Generate a complete, runnable pytest file.
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior automation engineer. Return only clean Python pytest code."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    

if __name__ == "__main__":
    

    client = JiraClient()
    story = client.extract_story_details('SCRUM-5')

    generator = AIGenerator()

    print("=" * 50)
    print("GENERATING TEST CASES...")
    print("=" * 50)
    test_cases = generator.generate_test_cases(story)
    print(test_cases)

    print("\n" + "=" * 50)
    print("GENERATING PLAYWRIGHT SCRIPT...")
    print("=" * 50)
    script = generator.generate_playwright_script(test_cases, story)
    print(script)

    #uv run python src/ai_generator.py