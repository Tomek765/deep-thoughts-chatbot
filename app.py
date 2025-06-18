from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Bot giełdowy działa. Wbij na /analyze."

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    ticker = data.get('ticker', '').upper()
    context = data.get('context', '')

    if not ticker:
        return jsonify({"error": "Brakuje tickera."}), 400

    prompt = (
        f"Jesteś brutalnym analitykiem giełdowym. Oceń spółkę {ticker} z GPW.\n"
        f"Kontekst: {context}\n"
        "Powiedz: POMPA, BURA, KONSOLA czy inna padaka. Strategia: 'Pump & Exit', '12% i spierdalaj'. Krótko i konkretnie."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return jsonify({"ticker": ticker, "analysis": response['choices'][0]['message']['content']})
