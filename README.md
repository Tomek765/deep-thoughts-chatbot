# Deep Thoughts Chatbot 🧠🌳

Bot prowadzony strukturą Deep Tree of Thoughts – krok po kroku do genialnych wniosków.

## 🔧 Lokalne uruchomienie

1. Utwórz plik `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

2. Zainstaluj zależności:
   ```
   pip install -r requirements.txt
   ```

3. Odpal lokalnie:
   ```
   uvicorn app:app --reload
   ```

4. Przetestuj:
   - POST na `http://localhost:8000/chat`  
     ```json
     {
       "user_message": "Chcę przemyśleć nową strategię marketingową.",
       "fast": false
     }
     ```

## ☁️ Deploy na Render.com

1. Zaloguj się i stwórz nowy Web Service z repo.
2. Wybierz typ `Python`, dodaj `OPENAI_API_KEY` jako zmienną środowiskową.
3. Render sam wciągnie `Procfile` i `.render.yaml`.
4. Done. Twój endpoint `/chat` działa w chmurze.

## ✍️ API

- `POST /chat`  
  **Request**:
  ```json
  {
    "user_message": "Twój tekst",
    "fast": false
  }
  ```
  **Response**:
  ```json
  {
    "bot_message": "Odpowiedź asystenta"
  }
  ```

- `GET /health` – status serwisu

## 📜 Licencja

Wolno kopiować, edytować, forki robić – byle z klasą i bez spamu.
