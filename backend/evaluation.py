from dotenv import load_dotenv

load_dotenv()

from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision
)

from datasets import Dataset


# =========================
# Sample Evaluation Data
# =========================

data = {

    "question": [
        "What is the leave policy?"
    ],

    "answer": [
        """
Employees receive annual leave,
sick leave and maternity leave.
"""
    ],

    "contexts": [[
        """
Privilege leave is 15-21 days.
Sick leave is 12 days.
Casual leave is 7 days.
"""
    ]],

    "ground_truth": [
        """
Employees get annual,
casual and sick leave.
"""
    ]
}


dataset = Dataset.from_dict(data)


# =========================
# Run Evaluation
# =========================

result = evaluate(

    dataset,

    metrics=[

        faithfulness,

        answer_relevancy,

        context_precision
    ]
)


print(result)