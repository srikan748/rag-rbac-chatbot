import csv

from datetime import datetime

from pathlib import Path

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    Form,
    Depends
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from fastapi.openapi.utils import (
    get_openapi
)

from jose import (
    jwt,
    JWTError
)

from backend.rag_pipeline import (

    load_documents,

    split_documents,

    create_vectorstore,

    create_qa_chain
)

# =========================
# LOAD ENV
# =========================

env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path)

# =========================
# FASTAPI APP
# =========================

app = FastAPI(

    title="Enterprise RAG RBAC Chatbot API",

    description="""
Enterprise AI Chatbot with:

- RAG
- JWT Authentication
- RBAC
- FAISS Vector Search
- Groq LLM
- Monitoring & Logging
""",

    version="1.0.0"
)

# =========================
# SECURITY
# =========================

security = HTTPBearer()

# =========================
# OPENAPI AUTH
# =========================

def custom_openapi():

    if app.openapi_schema:

        return app.openapi_schema

    openapi_schema = get_openapi(

        title="Enterprise RAG RBAC Chatbot API",

        version="1.0.0",

        description="Enterprise RAG API",

        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {

        "BearerAuth": {

            "type": "http",

            "scheme": "bearer",

            "bearerFormat": "JWT"
        }
    }

    openapi_schema["paths"]["/chat"]["post"]["security"] = [

        {

            "BearerAuth": []
        }
    ]

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi

# =========================
# CORS
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# =========================
# JWT CONFIG
# =========================

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

# =========================
# USERS
# =========================

fake_users = {

    "employee_user": {

        "password": "employee123",

        "role": "employee"
    },

    "hr_user": {

        "password": "hr123",

        "role": "hr"
    },

    "finance_user": {

        "password": "finance123",

        "role": "finance"
    },

    "marketing_user": {

        "password": "marketing123",

        "role": "marketing"
    },

    "engineering_user": {

        "password": "eng123",

        "role": "engineering"
    },

    "ceo_user": {

        "password": "ceo123",

        "role": "ceo"
    }
}

# =========================
# VECTORSTORE
# =========================

vectorstore = None

# =========================
# INITIALIZE RAG
# =========================

def initialize_rag():

    global vectorstore

    if vectorstore is None:

        BASE_DIR = Path(__file__).resolve().parent.parent

        DOCUMENTS_PATH = BASE_DIR / "documents"

        print("Loading documents...")

        documents = load_documents(
            str(DOCUMENTS_PATH)
        )

        print("Splitting documents...")

        chunks = split_documents(
            documents
        )

        print("Creating vectorstore...")

        vectorstore = create_vectorstore(
            chunks
        )

        print("RAG system ready.")

# =========================
# CREATE TOKEN
# =========================

def create_token(

    username,

    role
):

    payload = {

        "sub": username,

        "role": role
    }

    token = jwt.encode(

        payload,

        SECRET_KEY,

        algorithm=ALGORITHM
    )

    return token

# =========================
# VERIFY TOKEN
# =========================

def verify_token(token):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None

# =========================
# LOG CHAT
# =========================

def log_chat(

    username,

    role,

    question,

    answer,

    sources
):

    log_file = "logs/chat_logs.csv"

    with open(

        log_file,

        mode="a",

        newline="",

        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            datetime.now(),

            username,

            role,

            question,

            answer,

            ", ".join(sources)
        ])

# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {

        "message":
        "Enterprise RAG RBAC Chatbot Running Successfully"
    }

# =========================
# LOGIN
# =========================

@app.post("/login")
def login(

    username: str = Form(...),

    password: str = Form(...)
):

    if username not in fake_users:

        return {

            "error":
            "Invalid username"
        }

    user = fake_users[username]

    if password != user["password"]:

        return {

            "error":
            "Invalid password"
        }

    role = user["role"]

    token = create_token(

        username,

        role
    )

    return {

        "token": token,

        "role": role
    }

# =========================
# CHAT
# =========================

@app.post("/chat")
async def chat(

    question: str = Form(...),

    credentials:
    HTTPAuthorizationCredentials
    = Depends(security)
):

    try:

        # VERIFY TOKEN

        token = credentials.credentials

        user = verify_token(token)

        if user is None:

            return {

                "error":
                "Invalid token"
            }

        username = user["sub"]

        role = user["role"]

        # INITIALIZE RAG

        initialize_rag()

        # CREATE QA CHAIN

        qa_chain = create_qa_chain(

            vectorstore,

            role
        )

        # QUERY

        raw_result = qa_chain.invoke({

            "query": question
        })

        answer = raw_result["result"]

        # SOURCES

        sources = []

        for doc in raw_result["source_documents"]:

            source = doc.metadata.get(

                "source",

                "Unknown"
            )

            if source not in sources:

                sources.append(source)

        # LOGGING

        log_chat(

            username,

            role,

            question,

            answer,

            sources
        )

        # RESPONSE

        return {

            "answer": str(answer),

            "role": str(role),

            "sources": sources
        }

    except Exception as e:

        print("CHAT ERROR:")
        print(str(e))

        return {

            "error": str(e)
        }