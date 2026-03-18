import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

def analyze_email(email: str) -> dict[str, str]:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
        Jsi AI agent který analyzuje emaily.
        Dostaneš email a vrátíš POUZE JSON ve formátu:
        {
        "shrnutí": "...",
        "kategorie": "...",
        "akce": ["..."],
        "priorita": "..."
        }
        - kategorie emailu mohou být například: aktura / dotaz / stížnost / jiné
        - priorita: vysoká / střední / nízká
        - navrhni nejrozumnější akce na odpovězení na email
        Vracej pouze JSON, žádný extra text navíc není vyžadován.
        """
    response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=email,
                config=types.GenerateContentConfig(system_instruction=system_prompt)
                )

    raw = response.text
    raw = raw.replace("```", "")
    parsed = raw.replace("json", "")
    return json.loads(parsed)


def main() -> None:
    pass

if __name__ == '__main__':
    main()