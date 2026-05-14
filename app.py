import streamlit as st
from main import sync_and_analyze_emails
from database import init_db, get_history, get_latest_email_record

# Initialize database on startup
init_db()

st.set_page_config(page_title="AI Email Agent", page_icon="✉️", layout="centered")
st.title("AI Email Agent")
st.caption("Automated Gmail synchronization and two-step AI analysis (Fact Extraction → Structured Analysis).")

tab_sync, tab_history = st.tabs(["Inbox Sync", "History Log"])

with tab_sync:
    st.subheader("Fetch & Analyze New Emails")
    st.write("Connects to your Gmail inbox via REST API, skips already processed messages, and runs the Gemini AI production pipeline.")

    # Action button for synchronization
    if st.button("Sync Inbox", type="primary"):
        with st.spinner("Fetching latest emails from Gmail and running AI analysis..."):
            try:
                # Triggers the backend main.py pipeline with a safe test limit
                new_emails = sync_and_analyze_emails(limit=3)
                
                if new_emails > 0:
                    st.success(f"Sync complete! Successfully analyzed {new_emails} new email(s).")
                else:
                    st.info("No new emails found. Your database is completely up to date!")
            except Exception as e:
                st.error(f"Synchronization failed: {e}")
                st.stop()

    st.divider()

    # Automatically fetch and display the latest record from SQLite
    latest = get_latest_email_record()
    if latest:
        st.subheader("Latest Analyzed Email Insights")
        
        # Row 1 — Category, Priority, Sentiment metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Category", latest["category"].capitalize())
        col2.metric("Priority", latest["priority"].capitalize())
        col3.metric("Sentiment", latest["sentiment"].capitalize())

        # Dynamic priority banner based on severity level
        priority_level = latest["priority"].lower()
        reason = latest["priority_reason"]
        if priority_level == "high":
            st.error(f"**Why High Priority:** {reason}")
        elif priority_level == "medium":
            st.warning(f"**Why Medium Priority:** {reason}")
        else:
            st.success(f"**Why Low Priority:** {reason}")

        # Row 2 — Confidence score & Operational actionability
        col4, col5 = st.columns(2)
        col4.metric("AI Confidence", f"{float(latest.get('confidence', 0)):.0%}")
        col5.metric("Actionability State", latest.get("actionability", "").replace("_", " ").capitalize())

        # Row 3 — Response flags and deadline extraction
        col6, col7, col8 = st.columns(3)
        col6.metric("Requires Response", "Yes" if latest.get("requires_response") else "No")
        col7.metric("Follow Up Needed", "Yes" if latest.get("follow_up_needed") else "No")
        col8.metric("Extracted Deadline", latest.get("deadline") or "None")

        # Executive Summary section
        st.markdown("### Executive Summary")
        st.info(latest["summary"])

        # Specific Action Items checklist
        st.markdown("### Suggested Action Items")
        if latest.get("actions"):
            for i, action in enumerate(latest["actions"], 1):
                st.write(f"{i}. {action}")
        else:
            st.write("*No concrete action items detected.*")

        # Named Entity Recognition matrix
        entities = latest.get("entities", {})
        if isinstance(entities, dict) and any(entities.values()):
            st.markdown("### Extracted Entities")
            col9, col10, col11 = st.columns(3)
            
            with col9:
                st.write("**People**")
                for p in entities.get("people", []):
                    st.write(f"- {p}")
            with col10:
                st.write("**Companies**")
                for c in entities.get("companies", []):
                    st.write(f"- {c}")
            with col11:
                st.write("**Dates & References**")
                for d in entities.get("dates", []):
                    st.write(f"- {d}")
    else:
        st.info("The local database is currently empty. Click 'Sync Inbox' above to process your first live email.")

with tab_history:
    st.subheader("Historical Email Analyses")
    records = get_history()

    if not records:
        st.info("No historical records found in the database yet.")
    else:
        # Renders past records inside clean, collapsed accordion tabs
        for record in records:
            label = f"[{record['priority'].upper()}] {record['summary'][:75]}... — {record['timestamp']}"
            with st.expander(label):
                col1, col2, col3 = st.columns(3)
                col1.metric("Category", record["category"].capitalize())
                col2.metric("Priority", record["priority"].capitalize())
                col3.metric("Sentiment", record.get("sentiment", "").capitalize())

                if record.get("priority_reason"):
                    st.caption(f"**Priority Reason:** {record['priority_reason']}")

                col4, col5 = st.columns(2)
                col4.metric("AI Confidence", f"{float(record.get('confidence', 0)):.0%}")
                col5.metric("Actionability", record.get("actionability", "").replace("_", " ").capitalize())

                col6, col7, col8 = st.columns(3)
                col6.metric("Requires Response", "Yes" if record.get("requires_response") else "No")
                col7.metric("Follow Up Needed", "Yes" if record.get("follow_up_needed") else "No")
                col8.metric("Deadline", record.get("deadline") or "None")

                st.markdown("#### Summary")
                st.write(record["summary"])
                
                st.markdown("#### Action Items")
                for action in record.get("actions", []):
                    st.write(f"- {action}")

                entities = record.get("entities", {})
                if isinstance(entities, dict) and any(entities.values()):
                    st.markdown("#### Detected Entities")
                    col9, col10, col11 = st.columns(3)
                    with col9:
                        st.write("**People**")
                        for p in entities.get("people", []):
                            st.write(f"- {p}")
                    with col10:
                        st.write("**Companies**")
                        for c in entities.get("companies", []):
                            st.write(f"- {c}")
                    with col11:
                        st.write("**Dates**")
                        for d in entities.get("dates", []):
                            st.write(f"- {d}")