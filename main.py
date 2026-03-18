import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json


def main() -> None:
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

    emails = [
    "Dobrý den, posílám fakturu č. 2024-156 za konzultační služby v hodnotě 15 000 Kč. Prosím o úhradu do 14 dnů.",
    "Dobrý den, potřeboval bych od vás marketingový audit, už na něj čekám týden.",
    "Dobrý den, zajímalo by mě jaké služby nabízíte v oblasti SEO optimalizace."
    ]

    data = []
    try:
        for email in emails:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=email,
                config=types.GenerateContentConfig(system_instruction=system_prompt)
                )

            raw = response.text
            raw = raw.replace("```", "")
            parsed = raw.replace("json", "")
            data.append(json.loads(parsed))
    except genai.errors.ClientError as e:
        print(f"API chyba: {e}")
    except Exception as e:
        print(f"Neočekávaná chyba: {e}")

    if data:
        with open("output.json", "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    else:
        print("Žádná data k uložení.")

if __name__ == '__main__':
    main()