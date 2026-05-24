import streamlit as st

import requests

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(

    page_title=
    "Enterprise RAG Chatbot",

    page_icon="🤖",

    layout="wide"
)

# =========================
# TITLE
# =========================

st.title(
    "🤖 Enterprise RAG RBAC Chatbot"
)

st.markdown(
    """
Secure AI Assistant for:

- HR
- Finance
- Marketing
- Engineering
- Executives
"""
)

# =========================
# LOGIN
# =========================

st.sidebar.title(
    "🔐 Login"
)

username = st.sidebar.text_input(
    "Username"
)

password = st.sidebar.text_input(

    "Password",

    type="password"
)

login_button = st.sidebar.button(
    "Login"
)

# =========================
# LOGIN REQUEST
# =========================

if login_button:

    response = requests.post(

        "http://localhost:8080/login",

        data={

            "username": username,

            "password": password
        }
    )

    data = response.json()

    if "token" in data:

        st.session_state["token"] = data["token"]

        st.session_state["role"] = data["role"]

        st.success(
            f"Logged in as {data['role']}"
        )

    else:

        st.error(
            data["error"]
        )

# =========================
# CHAT SECTION
# =========================

if "token" in st.session_state:

    st.subheader(
        "💬 Ask Questions"
    )

    question = st.text_input(
        "Enter your question"
    )

    ask_button = st.button(
        "Ask AI"
    )

    if ask_button:

        response = requests.post(

            "http://localhost:8080/chat",

            headers={

                "Authorization":
                f"Bearer {st.session_state['token']}"
            },

            data={

                "question": question
            }
        )

        result = response.json()

        if "error" in result:

            st.error(
                result["error"]
            )

        else:

            st.success(
                "Answer Generated"
            )

            st.write(
                "### Answer"
            )

            st.write(
                result["answer"]
            )

            st.write(
                "### Role"
            )

            st.write(
                result["role"]
            )

            st.write(
                "### Sources"
            )

            for source in result["sources"]:

                st.write(
                    f"- {source}"
                )

else:

    st.info(
        "Please login first."
    )