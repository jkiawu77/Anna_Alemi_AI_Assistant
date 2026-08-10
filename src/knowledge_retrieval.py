import json
import re
from difflib import SequenceMatcher
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "knowledge_base.json"
)


INTENT_CATEGORY_MAP = {
    "buyer": "Buyer",
    "seller": "Seller",
    "investor": "Investor",
    "military_relocation": "Military Relocation",
    "ottawa_relocation": "Ottawa Relocation",
    "general_real_estate": "General Real Estate"
}


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "before",
    "can", "do", "for", "from", "how", "i", "in", "is",
    "it", "me", "my", "of", "on", "or", "should", "that",
    "the", "this", "to", "want", "what", "when", "where",
    "which", "why", "with", "you", "your"
}


def load_knowledge():
    """Load approved knowledge-base records."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["knowledge_base"]


def normalize_text(text):
    """Convert text into a clean lowercase form."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text):
    """Create meaningful search tokens."""
    normalized = normalize_text(text)

    return {
        word
        for word in normalized.split()
        if word not in STOP_WORDS and len(word) > 1
    }


def calculate_match_score(user_message, record):
    """Calculate similarity between a message and one knowledge record."""
    message_normalized = normalize_text(user_message)
    question_normalized = normalize_text(record.get("question", ""))

    message_tokens = tokenize(user_message)
    question_tokens = tokenize(record.get("question", ""))

    score = 0.0

    # 1. Keyword phrase matching
    for keyword in record.get("keywords", []):
        keyword_normalized = normalize_text(keyword)

        if keyword_normalized in message_normalized:
            score += 4.0

        else:
            keyword_tokens = tokenize(keyword)

            if keyword_tokens:
                overlap = len(message_tokens & keyword_tokens)
                score += overlap * 1.5

    # 2. Token overlap with the stored question
    if question_tokens:
        overlap = len(message_tokens & question_tokens)
        overlap_ratio = overlap / len(question_tokens)
        score += overlap_ratio * 5.0

    # 3. Whole-sentence similarity
    similarity = SequenceMatcher(
        None,
        message_normalized,
        question_normalized
    ).ratio()

    score += similarity * 4.0

    # 4. Strong bonus for near-exact question wording
    if question_normalized in message_normalized:
        score += 5.0

    return round(score, 2)


def retrieve_knowledge(
    user_message,
    detected_intent=None,
    minimum_score=2.0
):
    """
    Retrieve the closest approved knowledge-base response.

    The function first searches within the detected intent category.
    If no strong answer is found, it performs a controlled search
    across the complete approved knowledge base.
    """
    records = load_knowledge()

    expected_category = INTENT_CATEGORY_MAP.get(detected_intent)

    category_records = []

    if expected_category:
        category_records = [
            record
            for record in records
            if record.get("category") == expected_category
        ]

    # Use all records when no category match is available
    search_records = category_records or records

    best_record = None
    best_score = 0.0

    for record in search_records:
        score = calculate_match_score(user_message, record)

        if score > best_score:
            best_score = score
            best_record = record

    # Controlled fallback across all approved records
    if best_score < minimum_score and category_records:
        for record in records:
            score = calculate_match_score(user_message, record)

            if score > best_score:
                best_score = score
                best_record = record

    if best_record is None or best_score < minimum_score:
        return {
            "found": False,
            "answer": None,
            "human_review": True,
            "score": best_score,
            "message": (
                "No sufficiently relevant approved "
                "knowledge-base answer was found."
            )
        }

    return {
        "found": True,
        "id": best_record["id"],
        "category": best_record["category"],
        "question": best_record["question"],
        "answer": best_record["answer"],
        "human_review": best_record.get("human_review", False),
        "route_to": best_record.get("route_to", "ISA Team"),
        "score": best_score
    }


if __name__ == "__main__":
    test_messages = [
        (
            "Why is it useful to have mortgage approval "
            "before viewing properties?",
            "buyer"
        ),
        (
            "How does an agent support a family during a military move?",
            "military_relocation"
        ),
        (
            "I am thinking about putting my townhouse on the market.",
            "seller"
        )
    ]

    for message, intent in test_messages:
        result = retrieve_knowledge(
            message,
            detected_intent=intent
        )

        print("\nMessage:", message)
        print("Intent:", intent)
        print("Found:", result["found"])
        print("Match Score:", result["score"])

        if result["found"]:
            print("Knowledge ID:", result["id"])
            print("Matched Question:", result["question"])
            print("Answer:", result["answer"])
        else:
            print("Response:", result["message"])