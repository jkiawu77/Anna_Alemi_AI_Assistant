"""
Guardrails Module

This module prevents the AI assistant from providing
legal, tax, mortgage or financial advice.
Instead, it offers to connect the visitor with
the appropriate Anna Alemi Real Estate team member.
"""


PROHIBITED_TOPICS = {

    "legal": [
        "legal advice",
        "lawyer",
        "lawsuit",
        "can i sue",
        "should i sue",
        "break my purchase agreement",
        "break my contract"
    ],

    "tax": [
        "tax advice",
        "capital gains",
        "avoid taxes",
        "tax strategy",
        "property tax"
    ],

    "mortgage": [
        "which mortgage",
        "best mortgage",
        "recommend a mortgage",
        "which lender",
        "best lender",
        "financial advice",
        "investment advice",
        "interest rate should i choose",
        "which financing"
    ]
}


EDUCATIONAL_QUESTIONS = [

    "why should i get pre-approved",

    "what is mortgage pre approval",

    "what is mortgage pre-approval",

    "benefits of mortgage pre approval",

    "benefits of mortgage pre-approval",

    "why is pre approval important",

    "why is pre-approval important"

]


def check_guardrails(message):

    message = message.lower()


    # -----------------------------------------
    # Allow educational questions
    # -----------------------------------------

    for question in EDUCATIONAL_QUESTIONS:

        if question in message:

            return {

                "allowed": True,

                "topic": None,

                "message": ""

            }


    # -----------------------------------------
    # Escalate prohibited advice
    # -----------------------------------------

    for topic, keywords in PROHIBITED_TOPICS.items():

        for keyword in keywords:

            if keyword in message:

                return {

                    "allowed": False,

                    "topic": topic,

                    "message": (
                        "This question requires advice from a qualified "
                        "professional.\n\n"
                        "I can help connect you with the appropriate member "
                        "of the Anna Alemi Real Estate team.\n\n"
                        "Would you like me to arrange that connection?"
                    )

                }


    # -----------------------------------------
    # Continue normal workflow
    # -----------------------------------------

    return {

        "allowed": True,

        "topic": None,

        "message": ""

    }



if __name__ == "__main__":

    tests = [

        "Why should I get pre-approved?",

        "Which mortgage should I choose?",

        "Can I sue the seller?",

        "How do I avoid capital gains tax?"

    ]

    for t in tests:

        print()

        print(t)

        print(check_guardrails(t))