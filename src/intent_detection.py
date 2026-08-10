import json
import os


# ---------------------------------------------------------
# FILE PATH
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INTENTS_FILE = os.path.join(
    BASE_DIR,
    "data",
    "intent_keywords.json"
)

# ---------------------------------------------------------
# LOAD INTENTS
# ---------------------------------------------------------

def load_intents():
    """
    Load intent definitions from intents.json.
    """

    with open(INTENTS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["intents"]


# ---------------------------------------------------------
# INTENT DETECTION
# ---------------------------------------------------------

def detect_intent(user_message):
    """
    Detect the visitor's most likely real-estate intent.
    """

    message = user_message.lower()

    intents = load_intents()

    best_intent = "general_real_estate"
    best_score = 0
    best_route = "ISA Team"

    for item in intents:

        score = 0

        # ---------------------------------------------
        # KEYWORDS FROM intents.json
        # ---------------------------------------------

        for keyword in item.get("keywords", []):

            keyword_lower = keyword.lower()

            if keyword_lower in message:
                score += 2


        # ---------------------------------------------
        # BUYER CLUES
        # ---------------------------------------------

        if item["intent"] == "buyer":

            buyer_clues = [
                "buy",
                "buying",
                "buyer",
                "purchase",
                "looking for a home",
                "looking at homes",
                "looking for a house",
                "looking for a condo",
                "mortgage",
                "pre-approved",
                "preapproved",
                "pre-approval"
            ]

            for clue in buyer_clues:
                if clue in message:
                    score += 1


        # ---------------------------------------------
        # SELLER CLUES
        # ---------------------------------------------

        elif item["intent"] == "seller":

            seller_clues = [
                "sell",
                "selling",
                "seller",
                "list my home",
                "list my house",
                "home value",
                "house value",
                "home worth",
                "house worth"
            ]

            for clue in seller_clues:
                if clue in message:
                    score += 1


        # ---------------------------------------------
        # INVESTOR CLUES
        # ---------------------------------------------

        elif item["intent"] == "investor":

            investor_clues = [
                "invest",
                "investing",
                "investor",
                "investment",
                "investment property",
                "rental property",
                "rental income",
                "cash flow",
                "duplex",
                "triplex"
            ]

            for clue in investor_clues:
                if clue in message:
                    score += 1


        # ---------------------------------------------
        # MILITARY RELOCATION CLUES
        # ---------------------------------------------

        elif item["intent"] == "military_relocation":

            military_clues = [
                "military",
                "caf",
                "canadian armed forces",
                "posted",
                "posting",
                "military posting",
                "house hunting trip",
                "hht",
                "report for duty",
                "relocation benefits"
            ]

            for clue in military_clues:
                if clue in message:
                    score += 2


        # ---------------------------------------------
        # OTTAWA RELOCATION CLUES
        # ---------------------------------------------

        elif item["intent"] == "ottawa_relocation":

            ottawa_clues = [
                "moving to ottawa",
                "move to ottawa",
                "relocating to ottawa",
                "relocate to ottawa",
                "new to ottawa",
                "moving into ottawa"
            ]

            for clue in ottawa_clues:
                if clue in message:
                    score += 2


        # ---------------------------------------------
        # SELECT BEST INTENT
        # ---------------------------------------------

        if score > best_score:

            best_score = score
            best_intent = item["intent"]
            best_route = item.get("route_to", "ISA Team")


    return {
        "intent": best_intent,
        "score": best_score,
        "route_to": best_route
    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    test_message = (
        "Why should I get pre-approved before looking at homes?"
    )

    result = detect_intent(test_message)

    print("Message:", test_message)
    print("Detected Intent:", result["intent"])
    print("Match Score:", result["score"])
    print("Route:", result["route_to"])