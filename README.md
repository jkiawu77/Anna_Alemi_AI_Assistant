# 🏡 Anna Alemi AI Website Assistant

An AI-powered Real Estate Website Assistant developed as part of a Data Analytics & Artificial Intelligence Practicum project.

The assistant helps prospective buyers, sellers, investors, military families, and individuals relocating to Ottawa by providing intelligent responses, qualifying leads, and routing inquiries to the appropriate real estate team.

---

# Project Overview

This project demonstrates how Artificial Intelligence can improve customer engagement and lead management within the real estate industry.

The assistant can:

- 🏠 Assist Home Buyers
- 🏡 Support Home Sellers
- 💼 Guide Real Estate Investors
- 🎖️ Help Military Relocation Clients
- 📍 Assist Ottawa Relocation Clients
- 💬 Answer General Real Estate Questions

The system combines conversational AI, lead qualification, knowledge retrieval, and automated routing to create a professional client experience.

---

# Key Features

- AI-powered conversational assistant
- Intent Detection Engine
- Knowledge Base Retrieval
- Lead Qualification System
- Intelligent Routing Engine
- Human Handoff Summary
- Safety Guardrails
- Streamlit Web Application
- Structured JSON Knowledge Base

---

# System Architecture

```
Visitor
    │
    ▼
AI Website Assistant
    │
    ▼
Intent Detection
    │
    ▼
Knowledge Retrieval
    │
    ▼
Lead Qualification
    │
    ▼
Routing Engine
    │
    ▼
Human Agent
```

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core application |
| Streamlit | Web interface |
| JSON | Knowledge base |
| Git | Version control |
| GitHub | Source code repository |
| Streamlit Community Cloud | Application deployment |

---

# Project Structure

```
Anna_Alemi_AI_Assistant/
│
├── data/
│   ├── intent_keywords.json
│   ├── knowledge_base.json
│   ├── lead_questions.json
│   └── routing_rules.json
│
├── docs/
│   ├── Prototype_Design_Specification.docx
│   ├── Testing_Report.docx
│   └── User_Guide.docx
│
├── outputs/
│   └── sample_handoff.txt
│
├── src/
│   ├── app.py
│   ├── conversation_manager.py
│   ├── intent_detection.py
│   ├── knowledge_retrieval.py
│   ├── lead_collection.py
│   ├── lead_qualification.py
│   ├── routing_engine.py
│   ├── handoff_summary.py
│   ├── prompts.py
│   └── guardrails.py
│
├── tests/
├── requirements.txt
└── README.md
```

---

# Live Application

🌐 **Streamlit Demo**

https://anna-alemi-real-estate-ai.streamlit.app

---

# Future Enhancements

Future versions of this project may include:

- OpenAI GPT integration
- Voice interaction
- CRM integration (HubSpot / Salesforce)
- Appointment booking
- Property recommendation engine
- Analytics dashboard
- Email notifications
- Retrieval-Augmented Generation (RAG)

---

# Author

**James Bobby Kiawu**

Data Analytics & Artificial Intelligence

Practicum Project in fulfillment of my studies at Willis College, Ottawa, ON. 

Submitted to Chief Hamel & Anna Alemi (CEO, Anna Alemi Real Estate) https://annaalemi.com/ 

2026
