import datetime


# =========================
# Query Logging
# =========================

def log_query(

    username,

    role,

    question
):

    with open(

        "query_logs.txt",

        "a",

        encoding="utf-8"

    ) as file:

        file.write(

            f"\n[{datetime.datetime.now()}] "
            f"USER={username} "
            f"ROLE={role} "
            f"QUESTION={question}"
        )


# =========================
# Token Cost Tracking
# =========================

TOTAL_TOKENS = 0


def track_tokens(tokens_used):

    global TOTAL_TOKENS

    TOTAL_TOKENS += tokens_used

    print(

        f"\nTOTAL TOKENS USED: "
        f"{TOTAL_TOKENS}\n"
    )

    # =========================
    # Alert Threshold
    # =========================

    if TOTAL_TOKENS > 100000:

        print(

            "\nWARNING: TOKEN LIMIT EXCEEDED\n"
        )