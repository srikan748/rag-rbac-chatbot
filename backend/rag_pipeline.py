import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

template = "You are a helpful assistant. Answer the question based on the context.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

def load_documents(folder_path):
    documents = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                elif file.endswith(".csv"):
                    loader = CSVLoader(file_path)
                    docs = loader.load()
                elif file.endswith(".txt") or file.endswith(".md"):
                    loader = TextLoader(file_path, encoding="utf-8")
                    docs = loader.load()
                else:
                    continue
                department = os.path.basename(root)
                for doc in docs:
                    doc.metadata["department"] = department
                    doc.metadata["source"] = file
                documents.extend(docs)
            except Exception as e:
                print(f"Failed loading {file}: {e}")
    print(f"Loaded {len(documents)} documents")
    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    return chunks

def create_vectorstore(chunks):
    if len(chunks) == 0:
        raise ValueError("No document chunks created.")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("FAISS vectorstore created successfully")
    return vectorstore

def create_qa_chain(vectorstore, role):
    role_access = {
        "employee": ["general"],
        "hr": ["hr", "general"],
        "finance": ["finance", "general"],
        "marketing": ["marketing", "general"],
        "engineering": ["engineering", "general"],
        "executive": ["hr", "finance", "marketing", "engineering", "general", "executive"]
    }
    allowed_departments = role_access.get(role, ["general"])
    all_docs = vectorstore.similarity_search("", k=100)
    filtered_docs = [doc for doc in all_docs if doc.metadata.get("department", "") in allowed_departments]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    filtered_vectorstore = FAISS.from_documents(filtered_docs, embeddings)
    retriever = filtered_vectorstore.as_retriever(search_kwargs={"k": 10})
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY missing")
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain