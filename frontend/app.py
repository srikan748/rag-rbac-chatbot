import streamlit as st
import requests

st.set_page_config(page_title="FinSolve AI Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    .main-header {background: linear-gradient(90deg, #1e3a5f, #2196F3);padding: 20px;border-radius: 10px;color: white;text-align: center;margin-bottom: 20px;}
    .role-badge {background: #2196F3;color: white;padding: 5px 15px;border-radius: 20px;font-weight: bold;}
    .answer-box {background: #1e3a5f;color: white;padding: 20px;border-radius: 10px;border-left: 5px solid #2196F3;margin: 10px 0;}
    .source-box {background: #e8f5e9;color: #1a1a1a;padding: 10px;border-radius: 5px;margin: 5px 0;font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>FinSolve Technologies</h1>
    <h3>Enterprise RAG RBAC Chatbot</h3>
    <p>Secure AI Assistant for Department-Specific Insights</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Secure Login")
    st.markdown("---")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login", use_container_width=True)
    st.markdown("---")
    st.markdown("### Available Roles")
    st.markdown("**Executive** - Full Access")
    st.markdown("**Finance** - Finance Data")
    st.markdown("**Marketing** - Campaign Data")
    st.markdown("**HR** - Employee Data")
    st.markdown("**Engineering** - Tech Docs")
    st.markdown("**Employee** - General Info")

if login_button:
    response = requests.post("http://localhost:8080/login", data={"username": username, "password": password})
    data = response.json()
    if "token" in data:
        st.session_state["token"] = data["token"]
        st.session_state["role"] = data["role"]
        st.session_state["username"] = username
        st.rerun()
    else:
        st.sidebar.error("Invalid: " + data["error"])

if "token" in st.session_state:
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### Welcome, **{st.session_state['username']}**!")
    with col2:
        st.markdown(f"<span class='role-badge'>{st.session_state['role'].upper()}</span>", unsafe_allow_html=True)
    with col3:
        if st.button("Logout"):
            del st.session_state["token"]
            del st.session_state["role"]
            del st.session_state["username"]
            st.rerun()
    st.markdown("---")
    st.subheader("Ask Your Question")
    question = st.text_input("", placeholder="e.g. What is the leave policy?")
    ask_button = st.button("Ask AI")
    if ask_button and question:
        with st.spinner("Thinking..."):
            response = requests.post("http://localhost:8080/chat", headers={"Authorization": f"Bearer {st.session_state['token']}"}, data={"question": question})
            result = response.json()
        if "error" in result:
            st.error(result["error"])
        else:
            st.markdown("### Answer")
            st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Your Role")
                st.markdown(f"<span class='role-badge'>{result['role'].upper()}</span>", unsafe_allow_html=True)
            with col2:
                st.markdown("### Sources")
                for source in result["sources"]:
                    st.markdown(f'<div class="source-box">{source}</div>', unsafe_allow_html=True)
else:
    st.markdown("### Please login from the sidebar!")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Secure Access - JWT Authentication")
    with col2:
        st.info("Role Based - Department-specific data")
    with col3:
        st.info("AI Powered - RAG with Groq LLM")