from rag_pipeline import load_documents
from rag_pipeline import split_documents
from rag_pipeline import create_vectorstore
from rag_pipeline import create_qa_chain

from guardrails import contains_pii
from guardrails import is_out_of_scope


# Load Documents
docs = load_documents("documents")

print("Documents Loaded:", len(docs))


# Split Documents
chunks = split_documents(docs)

print("Chunks Created:", len(chunks))


# Create Vector Database
vectorstore = create_vectorstore(chunks)

print("Vector DB Created Successfully")


# Select User Role
role = input(
    "\nEnter role (hr / finance / marketing / executive): "
)


# Create QA Chain
qa_chain = create_qa_chain(
    vectorstore,
    role
)

print("QA Chain Ready")


# Chat Loop
while True:

    question = input("\nAsk Question: ")

    if question.lower() == "exit":
        break

    # =========================
    # Guardrails
    # =========================

    # PII Detection
    if contains_pii(question):

        print("\nBlocked: PII detected.")

        continue

    # Out-of-Scope Detection
    if is_out_of_scope(question):

        print(
            "\nI can answer only company-related questions."
        )

        continue

    # Get Response
    response = qa_chain.run(question)

    print("\nAnswer:\n")

    print(response)