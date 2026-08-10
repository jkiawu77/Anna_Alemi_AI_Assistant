from guardrails import check_guardrails
from intent_detection import detect_intent
from knowledge_retrieval import retrieve_knowledge
from lead_collection import get_lead_questions
from lead_qualification import qualify_lead
from routing_engine import get_route
from handoff_summary import create_handoff_summary


def process_message(message, lead_data=None):
    """Process a visitor message through the complete assistant workflow."""

    # 1. Guardrail check
    guardrail = check_guardrails(message)

    if not guardrail["allowed"]:
        return {
            "status": "escalate",
            "response": guardrail["message"],
            "topic": guardrail["topic"]
        }

    # 2. Detect intent
    intent_result = detect_intent(message)

    intent = intent_result["intent"]
    intent_score = intent_result["score"]

    # 3. Retrieve approved knowledge
    knowledge = retrieve_knowledge(
        message,
        detected_intent=intent
    )

    if knowledge["found"]:
        response = knowledge["answer"]

        if knowledge["human_review"]:
            response += (
                "\n\nA member of the Anna Alemi Real Estate team "
                "may need to review this topic with you."
            )
    else:
        response = (
            "I don't have an approved answer for that question "
            "in my current knowledge base."
        )

    # 4. Get lead questions
    lead_questions = get_lead_questions(intent)

    result = {
        "status": "continue",
        "intent": intent,
        "intent_score": intent_score,
        "response": response,
        "lead_questions": lead_questions
    }

    # 5. Qualify and route lead when lead data is available
    if lead_data:
        qualification = qualify_lead(lead_data)

        priority = qualification["priority"]
        lead_score = qualification["score"]

        routing = get_route(intent, priority)

        result["priority"] = priority
        result["lead_score"] = lead_score
        result["route_to"] = routing["route_to"]
        result["next_action"] = routing["next_action"]
        result["special_flags"] = routing.get("special_flags", [])

        # Add workflow results to lead data
        handoff_data = lead_data.copy()

        handoff_data["intent"] = intent
        handoff_data["priority"] = priority
        handoff_data["route_to"] = routing["route_to"]
        handoff_data["next_action"] = routing["next_action"]

        # 6. Generate team handoff summary
        result["handoff_summary"] = create_handoff_summary(
            handoff_data
        )

    return result


if __name__ == "__main__":

    test_message = (
        "Why should I get pre-approved before looking at homes?"
    )

    result = process_message(test_message)

    print("Status:", result["status"])
    print("Detected Intent:", result.get("intent"))
    print("Intent Score:", result.get("intent_score"))
    print("Response:", result.get("response"))
    print(
        "Lead Questions Available:",
        len(result.get("lead_questions", []))
    )