import streamlit as st
from main import analyze_email
from database import init_db, save_email

init_db()

st.title("AI EMAIL AGENT")
email = st.text_area("Paste email here")

if st.button("Analyze"):
    with st.spinner("Analyzing..."):
        result = analyze_email(email)
        akce_str = ", ".join(result["akce"])
        save_email(email, result["shrnutí"], result["kategorie"],
                   result["priorita"], akce_str)

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Kategorie", result['kategorie'])
        with col2:
            st.metric("Priorita", result['priorita'])

        st.info(result['shrnutí'])

        st.subheader("Doporučené akce")
        for akce in result['akce']:
            st.success(akce)