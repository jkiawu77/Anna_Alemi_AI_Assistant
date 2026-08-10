import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "routing_rules.json"


def load_routing_rules():
    """Load routing rules from JSON."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["routing_rules"]


def get_route(intent, priority):
    """Return routing information for a lead."""
    rules = load_routing_rules()

    for rule in rules:
        if rule["intent"] == intent:
            return {
                "intent": intent,
                "priority": priority,
                "route_to": rule["default_route"],
                "next_action": rule["recommended_next_action"],
                "special_flags": rule.get("special_flags", [])
            }

    return {
        "intent": intent,
        "priority": priority,
        "route_to": "ISA Team",
        "next_action": "Manual review required",
        "special_flags": []
    }


if __name__ == "__main__":

    result = get_route(
        intent="military_relocation",
        priority="High"
    )

    print("Intent:", result["intent"])
    print("Priority:", result["priority"])
    print("Route:", result["route_to"])
    print("Next Action:", result["next_action"])
    print("Special Flags:", result["special_flags"])