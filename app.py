from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Tomek GPT – Cyngiel AI</title>
    <style>
        body { font-family: Arial; margin: 50px; background: #111; color: #eee; }
        input, textarea { width: 100%; padding: 10px; margin-top: 10px; background: #222; color: #fff; border: none; }
        button { padding: 10px 20px; background: #28a; color: white; border: none; cursor: pointer; margin-top: 10px; }
        pre { background: #222; padding: 15px; margin-top: 20px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>💰 Tomek GPT – Cyngiel AI 💥</h1>
    <form id="chatForm">
        <textarea id="message" rows="4" placeholder="Napisz pytanie..."></textarea>
        <button type="submit">Wyślij</button>
    </form>
    <pre id="response"></pre>

    <script>
        const form = document.getElementById('chatForm');
        form.onsubmit = async (e) => {
            e.preventDefault();
            const msg = document.getElementById('message').value;
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg })
            });
            const data = await res.json();
            document.getElementById('response').innerText = data.response;
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_root():
    return HTML_PAGE

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_gpt(chat_input: ChatInput):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś giełdowym cwaniakiem z krwi i kości. Pomagasz Tomkowi zarobić 100k jak najszybciej. Nie pierdolisz. Dajesz konkret, strategię, ostrą gadkę i masz wyjebane na small talk. Styl: błyskotliwy, sarkastyczny, bez cenzury."},
                {"role": "user", "content": chat_input.message}
            ]
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
