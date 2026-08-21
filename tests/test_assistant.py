import json
import sys
from pathlib import Path
import unittest

# Allow Python to find the src folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.intent_detection import detect_intent
from src.guardrails import check_guardrails


TEST_CASES_FILE = PROJECT_ROOT / "tests" / "test_cases.json"


class TestAnnaAlemiAssistant(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(TEST_CASES_FILE, "r", encoding="utf-8") as file:
            cls.test_cases = json.load(file)

    def test_intent_detection(self):
        """Test whether major real estate intents are detected correctly."""

        for case in self.test_cases:

            if "expected_intent" not in case:
                continue

            with self.subTest(test_id=case["test_id"]):

                result = detect_intent(case["message"])

                self.assertEqual(
                    result["intent"],
                    case["expected_intent"]
                )

    def test_guardrail(self):
        """Test whether mortgage advice is safely escalated."""

        case = next(
            item for item in self.test_cases
            if item["category"] == "guardrail"
        )

        result = check_guardrails(case["message"])

        self.assertFalse(result["allowed"])


if __name__ == "__main__":
    unittest.main()