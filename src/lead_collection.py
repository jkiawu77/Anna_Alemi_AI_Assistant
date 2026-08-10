import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "lead_questions.json"


def load_questions():
    """Load lead collection questions."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["lead_questions"]


def get_lead_questions(intent):
    """Return questions associated with the detected intent."""
    question_groups = load_questions()

    for group in question_groups:
        if group["intent"] == intent:
            return group["questions"]

    return []


if __name__ == "__main__":
    test_intent = "buyer"

    questions = get_lead_questions(test_intent)

    print("Detected Intent:", test_intent)
    print("Total Questions:", len(questions))

    for number, question in enumerate(questions, start=1):
        print(f"{number}. {question}")