from src.jira_client import JiraClient
from src.ai_generator import AIGenerator
from src.script_runner import ScriptRunner
from src.report import ReportGenerator
from src.aws_handler import AWSHandler
import os


def run_pipeline(issue_key: str):
    print("\n" + "=" * 60)
    print(f"AI QA PIPELINE — {issue_key}")
    print("=" * 60)

    # Step 1: Fetch Jira story
    print("\n[1/4] Fetching Jira story...")
    jira = JiraClient()
    story = jira.extract_story_details(issue_key)
    print(f"Story: {story['summary']}")

    # Step 2: Generate test cases + script
    print("\n[2/4] Generating test cases with GPT-4o...")
    generator = AIGenerator()
    test_cases = generator.generate_test_cases(story)
    print("Test cases generated.")

    print("\n[3/4] Generating Playwright script...")
    script = generator.generate_playwright_script(test_cases, story)
    print("Script generated.")

    # Step 3: Save and run
    runner = ScriptRunner()
    filename = f"test_{issue_key.lower().replace('-', '_')}.py"
    filepath = runner.save_script(script, filename)
    result = runner.run_tests(filepath)

    # Step 4: Generate report
    print("\n[4/4] Generating HTML report...")
    report = ReportGenerator()
    report_path = report.generate(story, test_cases, script, result)

    # Step 5: Upload to S3
    print("\n[5/5] Uploading report to S3...")
    aws = AWSHandler()
    report_url = aws.upload_report(report_path, issue_key)

    print("\n" + "=" * 60)
    print(f"PIPELINE COMPLETE")
    print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}")
    print(f"Report: {report_path}")
    print(f"S3 URL: {report_url}")
    print("=" * 60)

    


if __name__ == "__main__":
    run_pipeline('SCRUM-5')