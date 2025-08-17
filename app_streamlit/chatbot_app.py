# app_streamlit/chatbot_app.py
import streamlit as st
import requests

st.set_page_config(page_title="Chatbot RAG", layout="centered")
st.title("🤖 Chatbot RAG - Projet Stage")

API_URL = st.text_input("Chat API URL", "http://localhost:8001/chat")

if "history" not in st.session_state:
    st.session_state.history = []

q = st.text_input("Pose ta question :", key="input")
if st.button("Envoyer") and q:
    payload = {"question": q}
    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        if resp.ok:
            res = resp.json()
            answer = res.get("answer", "")
            sources = res.get("sources", [])
            st.session_state.history.append((q, answer, sources))
        else:
            st.error(resp.text)
    except Exception as e:
        st.error(str(e))

for q, ans, sources in reversed(st.session_state.history):
    st.markdown(f"**Q:** {q}")
    st.markdown(f"**A:** {ans}")
    if sources:
        st.markdown("**Sources:**")
        for s in sources:
            st.markdown(f"- {s}")
    st.markdown("---")
