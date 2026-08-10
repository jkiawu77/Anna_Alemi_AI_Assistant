import uuid

import streamlit as st

from conversation_manager import process_message
from prompts import WELCOME_MESSAGE


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Anna Alemi AI Website Assistant",
    page_icon="🏡",
    layout="centered"
)


# ---------------------------------------------------------
# PROFESSIONAL STYLING
# ---------------------------------------------------------

st.markdown(
    """
<style>
.stApp {
    background-color: #f6f8fb;
}

.main .block-container {
    max-width: 950px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.brand-header {
    background: white;
    border: 1px solid #e1e6ed;
    border-radius: 18px;
    padding: 26px;
    margin-bottom: 22px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.05);
}

.brand-title {
    font-size: 2rem;
    font-weight: 750;
    margin-bottom: 6px;
}

.brand-subtitle {
    color: #667085;
    font-size: 1rem;
    line-height: 1.6;
}

.service-line {
    color: #44546a;
    font-size: 0.9rem;
    margin-top: 12px;
}

.summary-card {
    background: white;
    border: 1px solid #dfe5ec;
    border-radius: 18px;
    padding: 25px;
    margin-top: 20px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.06);
}

.summary-title {
    font-size: 1.35rem;
    font-weight: 750;
    margin-bottom: 18px;
}

.summary-label {
    color: #667085;
    font-size: 0.82rem;
    margin-bottom: 2px;
}

.summary-value {
    font-weight: 650;
    margin-bottom: 14px;
}

.status-high {
    background: #fde8e8;
    color: #a61b1b;
    border-radius: 18px;
    padding: 7px 14px;
    display: inline-block;
    font-weight: 750;
}

.status-medium {
    background: #fff2cc;
    color: #805b00;
    border-radius: 18px;
    padding: 7px 14px;
    display: inline-block;
    font-weight: 750;
}

.status-low {
    background: #e7f5ec;
    color: #176b36;
    border-radius: 18px;
    padding: 7px 14px;
    display: inline-block;
    font-weight: 750;
}

.referral-card {
    background: white;
    border-left: 5px solid #b7791f;
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.05);
}

div.stButton > button {
    border-radius: 11px;
    min-height: 44px;
    font-weight: 600;
}

[data-testid="stSidebar"] {
    background-color: #edf2f7;
}

.privacy-note {
    background: #f0f4f8;
    border-radius: 12px;
    padding: 14px;
    color: #5f6877;
    font-size: 0.84rem;
    margin-top: 20px;
}

.footer {
    text-align: center;
    color: #7b8491;
    font-size: 0.8rem;
    margin-top: 40px;
    line-height: 1.5;
}
</style>
""",
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# QUICK-ANSWER OPTIONS
# ---------------------------------------------------------

QUICK_OPTIONS = {
    "property_type": [
        "Detached home",
        "Townhouse",
        "Condominium",
        "Semi-detached home",
        "Other"
    ],
    "housing_preference": [
        "Buy",
        "Rent",
        "Still deciding"
    ],
    "timeline": [
        "Immediately",
        "Within 1–3 months",
        "Within 3–6 months",
        "Within 6–12 months",
        "More than 12 months"
    ],
    "selling_timeline": [
        "Immediately",
        "Within 1–3 months",
        "Within 3–6 months",
        "Within 6–12 months",
        "More than 12 months"
    ],
    "relocation_date": [
        "Within 1 month",
        "Within 1–3 months",
        "Within 3–6 months",
        "Within 6–12 months",
        "Not confirmed"
    ],
    "timeline_urgency": [
        "Urgent",
        "Within 1–3 months",
        "Within 3–6 months",
        "Flexible"
    ],
    "financing": [
        "Yes, I am pre-approved",
        "I have spoken with a lender",
        "Not yet",
        "I am paying without financing"
    ],
    "investment_experience": [
        "Yes, this is my first investment",
        "No, I have invested before"
    ],
    "house_hunting_trip": [
        "Yes, it is scheduled",
        "Not yet",
        "Not applicable"
    ],
    "property_status": [
        "Yes, currently listed",
        "No, not currently listed"
    ],
    "valuation_interest": [
        "Yes, I would like a valuation discussion",
        "Not at this time"
    ],
    "human_assistance": [
        "Yes, please contact me",
        "No, I only need general information"
    ]
}


# ---------------------------------------------------------
# HUMAN ESCALATION QUESTIONS
# ---------------------------------------------------------

ESCALATION_QUESTIONS = [
    {
        "field": "name",
        "question": "What is your full name?"
    },
    {
        "field": "email",
        "question": (
            "What is the best email address for the team to contact you?"
        )
    },
    {
        "field": "phone",
        "question": (
            "What phone number should the team use? "
            "You may type 'skip' if you prefer email only."
        )
    },
    {
        "field": "preferred_contact_time",
        "question": "What is the best time for the team to contact you?"
    },
    {
        "field": "referral_reason",
        "question": (
            "Please briefly describe the help you need from the team."
        )
    }
]


# ---------------------------------------------------------
# SESSION MANAGEMENT
# ---------------------------------------------------------

def initialize_session():
    """Create Streamlit session-state values."""

    defaults = {
        "messages": [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE
            }
        ],
        "initial_message": None,
        "questions": [],
        "question_index": 0,
        "lead_data": {},
        "collecting_lead": False,
        "completed": False,
        "final_result": None,
        "awaiting_escalation_consent": False,
        "collecting_escalation": False,
        "escalation_index": 0,
        "escalation_data": {},
        "escalation_topic": None,
        "escalation_reference": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_conversation():
    """Clear the current conversation."""

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()


def add_message(role, content):
    """Add a message to the conversation."""

    st.session_state.messages.append(
        {
            "role": role,
            "content": content
        }
    )


# ---------------------------------------------------------
# NORMAL LEAD WORKFLOW
# ---------------------------------------------------------

def start_conversation(user_message):
    """Process the visitor's opening message."""

    result = process_message(user_message)

    if result.get("status") == "escalate":
        st.session_state.escalation_topic = result.get(
            "topic",
            "professional review"
        )

        add_message(
            "assistant",
            result.get(
                "response",
                "This inquiry requires professional review."
            )
        )

        add_message(
            "assistant",
            (
                "Would you like me to prepare a connection request "
                "for the Anna Alemi Real Estate team?"
            )
        )

        st.session_state.awaiting_escalation_consent = True
        return

    add_message(
        "assistant",
        result.get(
            "response",
            "I can help with your real estate inquiry."
        )
    )

    st.session_state.initial_message = user_message
    st.session_state.questions = result.get("lead_questions", [])
    st.session_state.question_index = 0

    if st.session_state.questions:
        st.session_state.collecting_lead = True

        add_message(
            "assistant",
            st.session_state.questions[0]["question"]
        )

    else:
        st.session_state.completed = True
        st.session_state.final_result = result


def collect_lead_answer(user_answer):
    """Store one lead answer and move to the next question."""

    questions = st.session_state.questions
    index = st.session_state.question_index

    if index >= len(questions):
        return

    current_question = questions[index]
    field_name = current_question["field"]

    st.session_state.lead_data[field_name] = user_answer
    st.session_state.question_index += 1

    next_index = st.session_state.question_index

    if next_index < len(questions):
        add_message(
            "assistant",
            questions[next_index]["question"]
        )
    else:
        complete_lead_workflow()


def complete_lead_workflow():
    """Qualify, route and summarize the completed lead."""

    final_result = process_message(
        st.session_state.initial_message,
        st.session_state.lead_data
    )

    st.session_state.final_result = final_result
    st.session_state.collecting_lead = False
    st.session_state.completed = True

    priority = final_result.get("priority", "Not assigned")
    route = final_result.get("route_to", "ISA Team")
    next_action = final_result.get(
        "next_action",
        "A team member will review your inquiry."
    )

    add_message(
        "assistant",
        (
            "Thank you. Your preliminary real estate intake is complete.\n\n"
            f"**Lead priority:** {priority}\n\n"
            f"**Route:** {route}\n\n"
            f"**Next action:** {next_action}"
        )
    )


# ---------------------------------------------------------
# ESCALATION AND REFERRAL WORKFLOW
# ---------------------------------------------------------

def handle_escalation_consent(user_message):
    """Interpret whether the visitor accepts a human referral."""

    normalized = user_message.strip().lower()

    positive_terms = [
        "yes",
        "please",
        "connect me",
        "go ahead",
        "sure",
        "okay",
        "ok"
    ]

    negative_terms = [
        "no",
        "not now",
        "maybe later",
        "cancel"
    ]

    if any(term in normalized for term in positive_terms):
        st.session_state.awaiting_escalation_consent = False
        st.session_state.collecting_escalation = True
        st.session_state.escalation_index = 0

        add_message(
            "assistant",
            (
                "Certainly. I will collect a few details so the "
                "appropriate team member can follow up."
            )
        )

        add_message(
            "assistant",
            ESCALATION_QUESTIONS[0]["question"]
        )

    elif any(term in normalized for term in negative_terms):
        st.session_state.awaiting_escalation_consent = False
        st.session_state.completed = True

        add_message(
            "assistant",
            (
                "Understood. You may start a new conversation "
                "whenever you are ready."
            )
        )

    else:
        add_message(
            "assistant",
            (
                "Please reply with 'yes' to prepare the connection "
                "request, or 'no' if you do not want a referral."
            )
        )


def collect_escalation_answer(user_answer):
    """Collect one human-referral detail."""

    index = st.session_state.escalation_index

    if index >= len(ESCALATION_QUESTIONS):
        return

    current_question = ESCALATION_QUESTIONS[index]
    field_name = current_question["field"]

    if (
        field_name == "phone"
        and user_answer.strip().lower() == "skip"
    ):
        st.session_state.escalation_data[field_name] = "Email only"
    else:
        st.session_state.escalation_data[field_name] = user_answer

    st.session_state.escalation_index += 1
    next_index = st.session_state.escalation_index

    if next_index < len(ESCALATION_QUESTIONS):
        add_message(
            "assistant",
            ESCALATION_QUESTIONS[next_index]["question"]
        )
    else:
        complete_escalation_workflow()


def complete_escalation_workflow():
    """Create the structured human-referral request."""

    reference = f"ISA-{uuid.uuid4().hex[:8].upper()}"

    st.session_state.escalation_reference = reference
    st.session_state.collecting_escalation = False
    st.session_state.completed = True

    referral = {
        "reference_number": reference,
        "client_name": st.session_state.escalation_data.get(
            "name",
            "Not provided"
        ),
        "email": st.session_state.escalation_data.get(
            "email",
            "Not provided"
        ),
        "phone": st.session_state.escalation_data.get(
            "phone",
            "Not provided"
        ),
        "preferred_contact_time": (
            st.session_state.escalation_data.get(
                "preferred_contact_time",
                "Not provided"
            )
        ),
        "referral_reason": st.session_state.escalation_data.get(
            "referral_reason",
            "Not provided"
        ),
        "topic": st.session_state.escalation_topic,
        "priority": "Medium",
        "route_to": "ISA Team",
        "next_action": "Human follow-up required"
    }

    st.session_state.final_result = {
        "status": "escalated",
        "referral_summary": referral
    }

    add_message(
        "assistant",
        (
            "Thank you. Your connection request has been prepared.\n\n"
            f"**Reference number:** {reference}\n\n"
            "**Route:** ISA Team\n\n"
            "**Next action:** Human follow-up required."
        )
    )


# ---------------------------------------------------------
# INITIALIZE APPLICATION
# ---------------------------------------------------------

initialize_session()


# ---------------------------------------------------------
# BRAND HEADER
# ---------------------------------------------------------

st.markdown(
    """
<div class="brand-header">
<div class="brand-title">🏡 Anna Alemi Real Estate</div>

<div class="brand-subtitle">
AI Website Assistant designed to support prospective buyers,
sellers, investors, military families and clients relocating
to Ottawa.
</div>

<div class="service-line">
Buyer Services • Seller Services • Investment Support •
Military Relocation • Ottawa Relocation
</div>
</div>
""",
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.header("Conversation Status")

    if st.session_state.completed:
        st.success("Workflow completed")

    elif st.session_state.collecting_escalation:
        total = len(ESCALATION_QUESTIONS)
        collected = st.session_state.escalation_index

        st.warning(
            f"Connection request: {collected} of {total} details collected"
        )

        st.progress(collected / total)

    elif st.session_state.collecting_lead:
        total = len(st.session_state.questions)
        collected = st.session_state.question_index

        st.info(
            f"Lead intake: {collected} of {total} answers collected"
        )

        if total > 0:
            st.progress(collected / total)

    elif st.session_state.awaiting_escalation_consent:
        st.warning("Awaiting referral confirmation")

    else:
        st.info("Ready to assist")

    st.divider()

    if st.button(
        "Start New Conversation",
        use_container_width=True
    ):
        reset_conversation()

    st.markdown(
        """
<div class="privacy-note">
Please do not provide passwords, banking details,
government identification numbers or other highly
sensitive information.
</div>
""",
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# DISPLAY CONVERSATION
# ---------------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------
# QUICK-ANSWER BUTTONS
# ---------------------------------------------------------

if st.session_state.collecting_lead:
    current_index = st.session_state.question_index
    questions = st.session_state.questions

    if current_index < len(questions):
        current_field = questions[current_index]["field"]
        options = QUICK_OPTIONS.get(current_field, [])

        if options:
            st.caption(
                "Select an option or type your own answer below."
            )

            columns = st.columns(2)

            for option_index, option in enumerate(options):
                with columns[option_index % 2]:
                    if st.button(
                        option,
                        key=(
                            f"{current_field}_"
                            f"{current_index}_"
                            f"{option_index}"
                        ),
                        use_container_width=True
                    ):
                        add_message("user", option)
                        collect_lead_answer(option)
                        st.rerun()


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

user_input = st.chat_input("Type your message here...")

if user_input:
    add_message("user", user_input)

    if st.session_state.collecting_escalation:
        collect_escalation_answer(user_input)

    elif st.session_state.awaiting_escalation_consent:
        handle_escalation_consent(user_input)

    elif st.session_state.collecting_lead:
        collect_lead_answer(user_input)

    elif not st.session_state.completed:
        start_conversation(user_input)

    st.rerun()


# ---------------------------------------------------------
# LEAD SUMMARY CARD
# ---------------------------------------------------------

if (
    st.session_state.completed
    and st.session_state.final_result
    and st.session_state.final_result.get("handoff_summary")
):
    final_result = st.session_state.final_result
    summary = final_result["handoff_summary"]

    priority = final_result.get("priority", "Not assigned")
    route = final_result.get("route_to", "ISA Team")
    next_action = final_result.get(
        "next_action",
        "A team member will review the inquiry."
    )

    priority_class = {
        "High": "status-high",
        "Medium": "status-medium",
        "Low": "status-low"
    }.get(priority, "status-medium")

    client_type = (
        summary.get("intent", "Unknown")
        .replace("_", " ")
        .title()
    )

    st.markdown(
        f"""
<div class="summary-card">
<div class="summary-title">📋 Preliminary Lead Summary</div>

<div class="summary-label">Client</div>
<div class="summary-value">
{summary.get("client_name", "Not provided")}
</div>

<div class="summary-label">Client Type</div>
<div class="summary-value">{client_type}</div>

<div class="summary-label">Property Type</div>
<div class="summary-value">
{summary.get("property_type", "Not provided")}
</div>

<div class="summary-label">Preferred Location</div>
<div class="summary-value">
{summary.get("preferred_location", "Not provided")}
</div>

<div class="summary-label">Budget</div>
<div class="summary-value">
{summary.get("budget", "Not provided")}
</div>

<div class="summary-label">Timeline</div>
<div class="summary-value">
{summary.get("timeline", "Not provided")}
</div>

<div class="summary-label">Priority</div>
<div class="{priority_class}">{priority}</div>

<br><br>

<div class="summary-label">Assigned Route</div>
<div class="summary-value">{route}</div>

<div class="summary-label">Recommended Next Action</div>
<div class="summary-value">{next_action}</div>
</div>
""",
        unsafe_allow_html=True
    )

    with st.expander(
        "View Complete ISA Team Handoff Details",
        expanded=False
    ):
        for field, value in summary.items():
            label = field.replace("_", " ").title()
            st.write(f"**{label}:** {value}")


# ---------------------------------------------------------
# REFERRAL SUMMARY CARD
# ---------------------------------------------------------

if (
    st.session_state.completed
    and st.session_state.final_result
    and st.session_state.final_result.get("referral_summary")
):
    referral = st.session_state.final_result["referral_summary"]

    referral_topic = (
        referral.get("topic", "Professional Review")
        .replace("_", " ")
        .title()
    )

    st.markdown(
        f"""
<div class="referral-card">
<div class="summary-title">🤝 Human Connection Request</div>

<div class="summary-label">Reference Number</div>
<div class="summary-value">
{referral.get("reference_number", "Not provided")}
</div>

<div class="summary-label">Client</div>
<div class="summary-value">
{referral.get("client_name", "Not provided")}
</div>

<div class="summary-label">Topic</div>
<div class="summary-value">{referral_topic}</div>

<div class="summary-label">Assigned Route</div>
<div class="summary-value">
{referral.get("route_to", "ISA Team")}
</div>

<div class="summary-label">Next Action</div>
<div class="summary-value">
{referral.get("next_action", "Human follow-up required")}
</div>
</div>
""",
        unsafe_allow_html=True
    )

    with st.expander(
        "View Complete Team Referral Details",
        expanded=False
    ):
        for field, value in referral.items():
            label = field.replace("_", " ").title()
            st.write(f"**{label}:** {value}")


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
<div class="footer">
Anna Alemi Real Estate AI Website Assistant Prototype<br>
This assistant provides general information only.
Legal, tax, mortgage and individualized financial questions
require review by a qualified professional.
</div>
""",
    unsafe_allow_html=True
)