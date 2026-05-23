import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_community.document_loaders.csv_loader import (
    CSVLoader
)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain.chains import (
    RetrievalQA
)

from langchain_groq import (
    ChatGroq
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from langchain.prompts import (
    PromptTemplate
)

# =========================
# STRICT RBAC PROMPT
# =========================

template = """

You are an enterprise AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, say:

"I do not have access to that information."

Do NOT use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
"""

PROMPT = PromptTemplate(

    template=template,

    input_variables=[

        "context",

        "question"
    ]
)

# =========================
# LOAD DOCUMENTS
# =========================

def load_documents(folder_path):

    documents = []

    for root, dirs, files in os.walk(folder_path):

        for file in files:

            file_path = os.path.join(
                root,
                file
            )

            try:

                # PDF FILES
                if file.endswith(".pdf"):

                    loader = PyPDFLoader(
                        file_path
                    )

                    docs = loader.load()

                # CSV FILES
                elif file.endswith(".csv"):

                    loader = CSVLoader(
                        file_path
                    )

                    docs = loader.load()

                # TXT / MD FILES
                elif file.endswith(".txt") or file.endswith(".md"):

                    loader = TextLoader(

                        file_path,

                        encoding="utf-8"
                    )

                    docs = loader.load()

                else:

                    continue

                # =========================
                # METADATA
                # =========================

                department = os.path.basename(root)

                for doc in docs:

                    doc.metadata["department"] = department

                    doc.metadata["source"] = file

                documents.extend(docs)

            except Exception as e:

                print(
                    f"Failed loading {file}: {e}"
                )

    print(
        f"Loaded {len(documents)} documents"
    )

    return documents

# =========================
# SPLIT DOCUMENTS
# =========================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=50
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks"
    )

    return chunks

# =========================
# CREATE VECTORSTORE
# =========================

def create_vectorstore(chunks):

    if len(chunks) == 0:

        raise ValueError(
            "No document chunks created."
        )

    embeddings = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(

        chunks,

        embeddings
    )

    print(
        "FAISS vectorstore created successfully"
    )

    return vectorstore

# =========================
# CREATE QA CHAIN
# =========================

def create_qa_chain(

    vectorstore,

    role
):

    # =========================
    # ROLE ACCESS
    # =========================

    role_access = {

        "employee": [
            "general"
        ],

        "hr": [
            "hr",
            "general"
        ],

        "finance": [
            "finance",
            "general"
        ],

        "marketing": [
            "marketing",
            "general"
        ],

        "engineering": [
            "engineering",
            "general"
        ],

        "ceo": [
            "hr",
            "finance",
            "marketing",
            "engineering",
            "general",
            "executive"
        ]
    }

    allowed_departments = role_access.get(

        role,

        ["general"]
    )

    # =========================
    # FILTER DOCUMENTS
    # =========================

    all_docs = vectorstore.similarity_search(

        "",

        k=100
    )

    filtered_docs = []

    for doc in all_docs:

        department = doc.metadata.get(

            "department",

            ""
        )

        if department in allowed_departments:

            filtered_docs.append(doc)

    # =========================
    # TEMP VECTORSTORE
    # =========================

    embeddings = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    filtered_vectorstore = FAISS.from_documents(

        filtered_docs,

        embeddings
    )

    retriever = filtered_vectorstore.as_retriever(

        search_kwargs={"k": 4}
    )

    # =========================
    # GROQ
    # =========================

    groq_api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not groq_api_key:

        raise ValueError(
            "GROQ_API_KEY missing"
        )

    llm = ChatGroq(

        groq_api_key=groq_api_key,

        model_name=
        "llama-3.1-8b-instant"
    )

    # =========================
    # QA CHAIN
    # =========================

    qa_chain = RetrievalQA.from_chain_type(

        llm=llm,

        retriever=retriever,

        return_source_documents=True,

        chain_type_kwargs={

            "prompt": PROMPT
        }
    )

    return qa_chain