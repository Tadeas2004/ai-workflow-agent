# AI Email Agent

An AI-powered email analysis tool that extracts category, priority, and suggested actions from any email using a two-step reasoning pipeline.

## How it works

The agent runs two sequential LLM calls — this is what makes it an agent rather than a simple prompt wrapper:

1. **Extraction step** — Gemini reads the email and extracts structured facts: sender intent, urgency signals, and email type
2. **Analysis step** — Gemini uses those extracted facts as context to produce the full analysis: summary, category, priority with reasoning, and specific action items

This chain-of-thought approach produces more accurate prioritization and more specific action suggestions than a single prompt would.

## Tech stack

| Layer | Tech |
|---|---|
| AI | Gemini 2.5 Flash Lite (Google GenAI) |
| UI | Streamlit |
| Database | SQLite |
| Language | Python |

## Features

- Two-step AI reasoning chain (fact extraction → analysis)
- Priority reasoning — the AI explains *why* it assigned a priority level
- History tab — all past analyses stored in SQLite and browsable in the UI
- Color-coded priority (red / yellow / green)

## Setup

**Prerequisites:** Python 3.12+, Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))

```bash
git clone https://github.com/Tadeas2004/ai-email-agent.git
cd ai-email-agent

python3 -m venv venv
venv/bin/python3 -m pip install -r requirements.txt
```

Create a `.env` file:
```
GEMINI_API_KEY=your_key_here
```

Run:
```bash
venv/bin/streamlit run app.py
```

Open `http://localhost:8501`
