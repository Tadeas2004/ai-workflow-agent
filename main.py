import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types


def _call_gemini(client, prompt: str, system: str) -> dict:
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=system)
    )
    # Robustly extract JSON from response regardless of markdown fences
    text = response.text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])


def analyze_email(email: str) -> dict:
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Step 1: Extract key facts from the email
    extraction_system = """You are an email analysis assistant.
    Extract key facts from the email. Return ONLY valid JSON:
    {
    "sender_intent": "what the sender wants or is communicating",
    "urgency_signals": ["list", "of", "urgency", "phrases"],
    "email_type": "question|request|complaint|invoice|other"
    }"""

    facts = _call_gemini(client, email, extraction_system)

    # Step 2: Use extracted facts to produce a full structured analysis
    analysis_system = f"""You are an email analysis assistant.
    You have already extracted these facts from the email:
    {json.dumps(facts, indent=2)}

    Now produce a full analysis. Return ONLY valid JSON:
    {{
    "summary": "2-3 sentence summary of the email",
    "category": "invoice|inquiry|complaint|other",
    "priority": "high|medium|low",
    "priority_reason": "one sentence explaining why this priority level was chosen",
    "actions": ["specific action 1", "specific action 2", "specific action 3"]
    }}"""

    return _call_gemini(client, email, analysis_system)


def main() -> None:
    pass

if __name__ == "__main__":
    main()
