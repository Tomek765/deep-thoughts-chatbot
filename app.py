import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import openai

# === KONFIGURACJA ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Brakuje klucza OPENAI_API_KEY w zmiennych środowiskowych.")
openai.api_key = OPENAI_API_KEY

MODEL = "gpt-4"

SYSTEM_PROMPT = """
Zawsze działaj według struktury Deep Tree of Thoughts. Nie udzielaj odpowiedzi od razu – prowadz mnie przez proces decyzyjny krok po kroku:

1. Zapytaj: „Jaki problem chcesz dziś przeanalizować?”
2. Zapytaj: „Na ile szczegółowo mam myśleć?”
   - Quick View
   - Balanced
   - Deep Dive
3. Zapytaj: „Na czym chcesz się skupić?”
   - Strategia, Potencjał, Bariery, Szybkie wygrane, Zasoby
4. Wygeneruj 3–5 pomysłów (Idea-1, Idea-2...)
5. Zrób podsumowanie (ocena potencjału, trudność, powiązania)

Nie przeskakuj żadnego etapu, nawet jeśli pytanie wygląda na oczywiste. Zawsze prowadź analizę spokojnie, jak dobry mentor.
Jeśli poproszę „szybko”, pomiń pytania i przejdź od razu do generowania pomysłów, ale nadal opieraj się na strukturze Deep Tree of Thoughts.
"""

app = FastAPI()

# === MODELE DANYCH ===
class RequestBody(BaseModel):
    user_message: str
    fast: bool = False  # opcjonalne "szybko"

class ResponseBody(BaseModel):
    bot_message: str

# === ENDPOINT ===
@app.post("/chat", response_model=ResponseBody)
async def chat_endpoint(body: RequestBody):
    """
    Przyjmuje {"user_message": "...", "fast": false}
    Zwraca {"bot_message": "..."}
    """
    # Buduj prompt
    try:
        resp = await openai.ChatCompletion.acreate(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT if not body.fast else ""},
                {"role": "user", "content": body.user_message}
            ],
            temperature=0.7,
            max_tokens=500,
        )
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {e}")
    answer = resp.choices[0].message.content.strip()
    return JSONResponse(content={"bot_message": answer})

# === HEALTH CHECK ===
@app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"})
