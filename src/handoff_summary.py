def create_handoff_summary(lead):
    summary = {
        "client_name": lead.get("name", lead.get("client_name", "Not provided")),
        "intent": lead.get("intent", "Unknown"),
        "priority": lead.get("priority", "Unknown"),
        "property_type": lead.get("property_type", "Not provided"),
        "preferred_location": lead.get("preferred_location", "Not provided"),
        "budget": lead.get("budget", "Not provided"),
        "timeline": lead.get("timeline", "Not provided"),
        "contact": lead.get("contact", "Not provided"),
        "route_to": lead.get("route_to", "ISA Team"),
        "next_action": lead.get("next_action", "Follow up with client")
    }

    return summary


if __name__ == "__main__":

    test_lead = {
        "name": "Test Client",
        "intent": "military_relocation",
        "priority": "High",
        "property_type": "Detached home",
        "preferred_location": "Ottawa",
        "budget": "$700,000",
        "timeline": "Within 3 months",
        "contact": "test@example.com",
        "route_to": "ISA Team - Military Relocation",
        "next_action": "Priority ISA Team military relocation follow-up"
    }

    summary = create_handoff_summary(test_lead)

    print("=== ISA TEAM HANDOFF SUMMARY ===")

    for key, value in summary.items():
        print(f"{key}: {value}")