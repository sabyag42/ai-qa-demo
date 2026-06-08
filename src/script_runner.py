import os
import subprocess
from dotenv import load_dotenv
from src.jira_client import JiraClient
from src.ai_generator import AIGenerator

load_dotenv()

class ScriptRunner:

    def __init__(self, output_dir: str = "tests"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save_script(self, script: str, filename: str) -> str:
        # Clean up markdown code blocks if GPT added them
        script = script.replace("```python", "").replace("```", "").strip()

        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(script)

        print(f"Script saved to: {filepath}")
        return filepath

    def run_tests(self, filepath: str) -> dict:
        print(f"\nRunning tests: {filepath}")
        print("=" * 50)

        result = subprocess.run(
            ["uv", "run", "pytest", filepath, "-v",
             "--tb=short", "--no-header"],
            capture_output=False,
            text=True
        )

        return {
            "returncode": result.returncode,
            "passed": result.returncode == 0
        }


# Quick test
if __name__ == "__main__":
    

    # Fetch story
    client = JiraClient()
    story = client.extract_story_details('SCRUM-5')

    # Generate test cases and script
    generator = AIGenerator()
    test_cases = generator.generate_test_cases(story)
    script = generator.generate_playwright_script(test_cases, story)

    # Save and run
    runner = ScriptRunner()
    filepath = runner.save_script(script, "test_scrum5.py")
    result = runner.run_tests(filepath)

    print("\n" + "=" * 50)
    if result['passed']:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")


#uv run python src/script_runner.py