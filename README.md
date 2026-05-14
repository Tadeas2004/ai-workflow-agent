# AI Email Agent

An AI-powered email analysis tool that reads any email and returns a structured breakdown — category, priority with reasoning, summary, and specific action items — using a two-step reasoning pipeline built on Gemini 2.5 Flash Lite.

**Live demo:** [ai-email-agent-9n28.onrender.com](https://ai-email-agent-9n28.onrender.com)

---

![Screenshot placeholder](https://via.placeholder.com/900x500?text=Screenshot+coming+soon)

---

## What it does

Paste any email and the agent runs two sequential AI calls:

1. **Extraction** — identifies sender intent, urgency signals, and email type
2. **Analysis** — uses those extracted facts to produce a full structured report

**Output:**
- Category — `invoice`, `inquiry`, `complaint`, or `other`
- Priority — `high`, `medium`, or `low` with a one-sentence explanation of why
- Summary — 2-3 sentence overview of the email
- Suggested actions — 3 specific next steps to take

**History tab** — every analysis is saved to a local SQLite database and browsable in the UI, with priority color-coding (red / yellow / green).

---

## Tech stack

| Layer | Tech |
|---|---|
| AI model | Gemini 2.5 Flash Lite (`google-genai`) |
| UI | Streamlit |
| Database | SQLite |
| Language | Python 3.12 |

---

## Run locally

**Prerequisites:** Python 3.12+, a free Gemini API key from [aistudio.google.com](https://aistudio.google.com)

```bash
git clone https://github.com/Tadeas2004/ai-email-agent.git
cd ai-email-agent

python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
```

Run the app:

```bash
venv/bin/streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## Deploy on Render

1. Push the project to a GitHub repository
2. Go to [render.com](https://render.com) and create a new **Web Service**
3. Connect your GitHub repo
4. Set the following:

| Field | Value |
|---|---|
| Environment | `Python` |
| Build command | `pip install -r requirements.txt` |
| Start command | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |

5. Add an environment variable in the Render dashboard:

```
GEMINI_API_KEY=your_key_here
```

6. Click **Deploy** — Render will build and host the app automatically.

> Note: The free Render tier spins down after inactivity. First load may take ~30 seconds to wake up.
