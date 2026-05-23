import re


# =========================
# PII Detection
# =========================

def contains_pii(text):

    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

    phone_pattern = r"\b\d{10}\b"

    credit_card_pattern = r"\b\d{16}\b"

    if re.search(email_pattern, text):

        return True

    if re.search(phone_pattern, text):

        return True

    if re.search(credit_card_pattern, text):

        return True

    return False


# =========================
# Out Of Scope Detection
# =========================

def is_out_of_scope(question):

    allowed_keywords = [

        "company",
        "employee",
        "finance",
        "marketing",
        "payroll",
        "budget",
        "sales",
        "hr",
        "report",
        "revenue",
        "expense"
    ]

    question = question.lower()

    for keyword in allowed_keywords:

        if keyword in question:

            return False

    return True