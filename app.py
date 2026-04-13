import streamlit as st
from main import analyze_email
from database import init_db, save_email, get_history

init_db()

st.set_page_config(page_title="Email Agent", page_icon="✉️", layout="centered")
st.title("AI Email Agent")
st.caption("Paste any email and the agent will analyze it in two steps: fact extraction → full analysis.")

tab_analyze, tab_history = st.tabs(["Analyze", "History"])

with tab_analyze:
    email = st.text_area("Email content", height=200, placeholder="Paste the email text here...")

    if st.button("Analyze", type="primary", disabled=not email.strip()):
        with st.spinner("Step 1: Extracting facts...  Step 2: Analyzing..."):
            try:
                result = analyze_email(email)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.stop()

        save_email(
            email=email,
            summary=result["summary"],
            category=result["category"],
            priority=result["priority"],
            priority_reason=result.get("priority_reason", ""),
            actions=str(result["actions"]),
        )

        st.divider()

        col1, col2 = st.columns(2)
        col1.metric("Category", result["category"].capitalize())
        col2.metric("Priority", result["priority"].capitalize())

        priority = result["priority"].lower()
        reason = result.get("priority_reason", "")
        if priority == "high":
            st.error(f"**Why high priority:** {reason}")
        elif priority == "medium":
            st.warning(f"**Why medium priority:** {reason}")
        else:
            st.success(f"**Why low priority:** {reason}")

        st.subheader("Summary")
        st.write(result["summary"])

        st.subheader("Suggested Actions")
        for i, action in enumerate(result["actions"], 1):
            st.write(f"{i}. {action}")

with tab_history:
    st.subheader("Past Analyses")
    records = get_history()

    if not records:
        st.info("No emails analyzed yet.")
    else:
        for record in records:
            label = f"[{record['priority'].upper()}]  {record['summary'][:80]}...  —  {record['timestamp']}"
            with st.expander(label):
                col1, col2 = st.columns(2)
                col1.metric("Category", record["category"].capitalize())
                col2.metric("Priority", record["priority"].capitalize())
                st.write(record["summary"])
                if record.get("priority_reason"):
                    st.caption(f"Priority reason: {record['priority_reason']}")
                st.write("**Suggested Actions:**")
                for action in record["actions"]:
                    st.write(f"- {action}")
