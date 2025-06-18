from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Bot giełdowy działa. Wbij na /analyzo."

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    ticker = data.get('ticker', '').upper()
    context = data.get('context', '')

    if not ticker:
        return jsonify({"error": "Brakuje tickera."}), 400

    prompt = f"Jesteś brutalnym analitykiem giełdowym. Sprawdź spółkę {ticker}. Kontekst: {context}. Oceń czy warto kupić, sprzedać czy trzymać. Nie gadaj głupot, tylko konkrety."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"recommendation": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
