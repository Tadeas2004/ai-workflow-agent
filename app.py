import streamlit as st
from main import analyze_email

st.title("AI EMAIL AGENT")
email = st.text_area("Paste email here")

if st.button("Analyze"):
    with st.spinner("Analyzing..."):
        result = analyze_email(email)
    st.json(result)