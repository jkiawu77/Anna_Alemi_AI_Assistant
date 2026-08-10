def qualify_lead(lead_data):
    """Assign a lead priority based on readiness signals."""

    score = 0

    timeline = lead_data.get("timeline", "").lower()
    financing = lead_data.get("financing", "").lower()
    contact = lead_data.get("contact", "")
    budget = lead_data.get("budget", "")

    # Timeline
    if any(term in timeline for term in ["1 month", "2 months", "3 months", "immediately", "as soon as possible"]):
        score += 3
    elif any(term in timeline for term in ["4 months", "6 months", "within a year"]):
        score += 2

    # Financing readiness
    if "pre-approved" in financing or "preapproved" in financing:
        score += 3

    # Budget supplied
    if budget:
        score += 1

    # Contact information supplied
    if contact:
        score += 2

    if score >= 7:
        priority = "High"
    elif score >= 3:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "priority": priority,
        "score": score
    }


if __name__ == "__main__":

    test_lead = {
        "timeline": "within 2 months",
        "financing": "I am pre-approved",
        "budget": "$650,000",
        "contact": "client@example.com"
    }

    result = qualify_lead(test_lead)

    print("Lead Score:", result["score"])
    print("Lead Priority:", result["priority"])