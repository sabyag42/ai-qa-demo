# AI QA Demo — Intelligent Test Automation Pipeline

An AI-powered end-to-end test automation pipeline that automatically generates, 
executes, and reports on test cases using Jira, OpenAI GPT-4o, and Playwright.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Playwright](https://img.shields.io/badge/Playwright-Latest-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange)
![Jira](https://img.shields.io/badge/Jira-REST%20API-blue)

## What It Does

Jira Story → GPT-4o generates test cases → GPT-4o generates Playwright script
→ Tests execute automatically → HTML report opens in browser


## Demo Flow

1. Fetch a Jira user story via REST API
2. GPT-4o reads the story and writes structured test cases
3. GPT-4o converts test cases into a Playwright Python script
4. Script executes automatically with pytest
5. HTML report renders with full results

## Tech Stack

- **Python 3.11** — core language
- **uv** — package management
- **OpenAI GPT-4o** — test case + script generation
- **Playwright** — browser automation
- **pytest** — test runner
- **Jira REST API** — user story fetching
- **GitHub Actions** — CI/CD pipeline
- **AWS S3** — report storage
- **AWS SNS** — failure notifications

- ai-qa-demo/
├── src/
│   ├── init.py
│   ├── jira_client.py      # Jira REST API client
│   ├── ai_generator.py     # GPT-4o test + script generator
│   ├── script_runner.py    # pytest executor
│   └── report.py           # HTML report generator
├── tests/                  # AI generated test files
├── reports/                # HTML reports
├── main.py                 # Pipeline orchestrator
├── pytest.ini              # pytest configuration
├── pyproject.toml          # uv project config
└── .env                    # credentials (gitignored)


## Setup

### Prerequisites

- Python 3.11+
- uv installed — `pip install uv`
- AWS CLI configured — `aws configure`
- Jira account with API token
- OpenAI API key

### Installation

```bash
# Clone the repo
git clone https://github.com/sabyag42/ai-qa-demo.git
cd ai-qa-demo

# Install dependencies
uv sync

# Install Playwright browsers
uv run playwright install chromium
```

### Environment Variables

Create a `.env` file in the project root:



## Project Structure

JIRA_DOMAIN=your-domain.atlassian.net
JIRA_EMAIL=your-email@gmail.com
JIRA_API_TOKEN=your-jira-api-token
OPENAI_API_KEY=your-openai-api-key

### Getting a Jira API Token

1. Go to https://id.atlassian.com/manage-api-tokens
2. Click **Create API token**
3. Copy the token into `.env`

### Getting an OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Click **Create new secret key**
3. Copy the key into `.env`

## Running the Pipeline

### Full Pipeline — Single Command

```bash
uv run python main.py
```

This will:
1. Fetch SCRUM-5 from Jira
2. Generate test cases with GPT-4o
3. Generate Playwright script with GPT-4o
4. Execute tests with pytest
5. Open HTML report in browser

### Run Against a Different Jira Issue

Edit the last line of `main.py`:

```python
if __name__ == "__main__":
    run_pipeline('SCRUM-5')  # change to any issue key
```

### Run Only the Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run smoke tests only
uv run pytest tests/ -v -m smoke

# Run regression tests only
uv run pytest tests/ -v -m regression

# Run specific test file
uv run pytest tests/test_scrum_5.py -v
```

### Run Individual Components

```bash
# Test Jira connection
uv run python src/jira_client.py

# Test AI generation
uv run python src/ai_generator.py

# Test script runner
uv run python src/script_runner.py
```

## CI/CD Pipeline

Tests run automatically on every push to `main` via GitHub Actions.

### Pipeline Steps

1. Checkout code
2. Install Python + uv
3. Install dependencies
4. Install Playwright browsers
5. Run full AI QA pipeline
6. Upload HTML report to AWS S3
7. Send SNS notification (pass or fail)
8. Upload report as GitHub artifact

### GitHub Secrets Required

| Secret | Description |
|---|---|
| `JIRA_DOMAIN` | Your Jira domain |
| `JIRA_EMAIL` | Your Jira email |
| `JIRA_API_TOKEN` | Jira API token |
| `OPENAI_API_KEY` | OpenAI API key |
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | AWS region e.g. us-east-1 |
| `S3_BUCKET_NAME` | S3 bucket for reports |
| `SNS_TOPIC_ARN` | SNS topic for notifications |

## Test Coverage

AI generates tests based on acceptance criteria. For SCRUM-5:

| Test | Type |
|---|---|
| Valid login | @smoke @regression |
| Invalid credentials | @regression |
| Empty fields | @regression |
| Locked out user | @regression |
| Password only | @regression |
| Username only | @regression |
| Special characters | @regression |
| SQL injection | @regression |

## Interview Talking Points

- **"How does the AI generate tests?"** — GPT-4o reads the Jira story summary and acceptance criteria, then generates structured test cases and converts them to executable Playwright Python code
- **"What if the AI generates wrong assertions?"** — The pipeline catches failures and reports them. We iterate on the prompt to improve accuracy
- **"How do you handle CI/CD?"** — GitHub Actions runs the full pipeline on every push, uploads reports to S3, and sends SNS notifications on failure
- **"What's next?"** — Self-healing selectors, visual regression, multi-story batch processing

## Author

Sabyasachi Ghosh — Senior SDET & Generative AI Engineer
- GitHub: [@sabyag42](https://github.com/sabyag42)
- LinkedIn: [Sabyasachi Ghosh](https://linkedin.com/in/sabyasachi-ghosh)

