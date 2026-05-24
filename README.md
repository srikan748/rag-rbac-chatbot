

# FinSolve Technologies - Enterprise RAG RBAC Chatbot

## Live Demo
- Live App: https://ragpulse-x7-rag-rbac-chatbots.hf.space
- GitHub: https://github.com/srikan748/rag-rbac-chatbot

## Project Overview

Built as part of the Codebasics Resume Project Challenge, this project solves a real-world problem faced by FinSolve Technologies - a leading FinTech company where teams were facing delays in communication and difficulty accessing the right data at the right time.

The solution is an AI-powered RAG-based chatbot with Role-Based Access Control (RBAC) that delivers secure, department-specific insights to employees across Finance, HR, Marketing, Engineering, and Executive teams.

## Problem Statement

FinSolve Technologies faced:
- Delays in communication between departments
- Data silos between Finance, Marketing, HR, and C-Level Executives
- Roadblocks in decision-making and strategic planning

Solution: A secure RBAC chatbot that gives each team access to only their relevant data, on demand, in natural language.

## Live Demo Credentials

| Role | Username | Password | Access |
|------|----------|----------|--------|
| Employee | employee_user | employee123 | General company info |
| HR | hr_user | hr123 | HR + General |
| Finance | finance_user | finance123 | Finance + General |
| Marketing | marketing_user | marketing123 | Marketing + General |
| Engineering | engineering_user | eng123 | Engineering + General |
| Executive | executive_user | executive123 | Full access to all data |

## Architecture

User Login (Streamlit UI)
|
JWT Authentication (FastAPI)
|
Role Detection (RBAC Engine)
|
Department Document Filtering
|
FAISS Vector Search
|
Groq LLM - Llama 3.1 Response Generation
|
Answer + Source Documents returned to User


## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Groq - Llama 3.1-8b-instant |
| Vector Store | FAISS |
| Embeddings | HuggingFace sentence-transformers |
| Authentication | JWT - JSON Web Tokens |
| Deployment | Hugging Face Spaces - Docker |
| Language | Python 3.10 |

## Roles and Permissions

| Role | Department Access |
|------|------------------|
| Employee | General only - policies, FAQs, events |
| HR | HR data + General |
| Finance | Financial reports + General |
| Marketing | Campaign data + General |
| Engineering | Technical docs + General |
| Executive | All departments - full access |

## Security Features

- JWT Authentication - Secure token-based login system
- Role-Based Access Control - Each role sees only permitted documents
- Department-level filtering - Documents filtered before vector search
- Secure API endpoints - Bearer token required for all chat requests
- Environment variables - All API keys stored as secrets

## Project Structure

rag-rbac-chatbot/
├── backend/
│   ├── main.py              # FastAPI app, JWT auth, RBAC logic
│   ├── rag_pipeline.py      # RAG pipeline, FAISS, embeddings
│   ├── auth.py              # Authentication helpers
│   ├── guardrails.py        # Input and output guardrails
│   ├── monitoring.py        # Logging and monitoring
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── app.py               # Streamlit UI
├── documents/
│   ├── general/             # Employee level documents
│   ├── hr/                  # HR department documents
│   ├── finance/             # Finance department documents
│   ├── marketing/           # Marketing department documents
│   └── engineering/         # Engineering department documents
├── Dockerfile               # Docker deployment configuration
└── README.md

## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/srikan748/rag-rbac-chatbot
cd rag-rbac-chatbot
```

### 2. Install dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Create .env file inside backend folder

GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key_here

### 4. Run the backend
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8080
```

### 5. Run the frontend
```bash
streamlit run frontend/app.py
```

## Key Features

- Natural language query processing
- Role-based document access control
- RAG pipeline with FAISS vector search
- Source document references in every response
- JWT-based secure authentication
- Chat logging and monitoring
- Docker deployment ready
- Live deployment on Hugging Face Spaces

## Author

**Srikanth Gunji**

Built with passion as part of Codebasics Resume Project Challenge

- LinkedIn: www.linkedin.com/in/gunji-srikanth91
- GitHub: https://github.com/srikan748

## Acknowledgements

- Codebasics for the amazing project challenge
- Groq for the fast LLM API
- LangChain for the RAG framework
- Hugging Face for free deployment

