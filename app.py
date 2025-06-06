import requests
import json
import os
from flask import Flask, render_template, request

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Ollama Configuration ---
OLLAMA_API_BASE_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL_NAME = "gemma:2b" # As per your satisfaction with Gemma 2B

# --- Personality Prediction Function (Modified for Flask) ---
def predict_personality_ollama(movie, music, cartoon, hobby, place, timepass):
    user_profile = f"""
    Favorite Movie: {movie}
    Favorite Music Genre: {music}
    Favorite Cartoon: {cartoon}
    Hobby: {hobby}
    Favorite Place: {place}
    Favorite Timepass Activity: {timepass}
    """
    prompt = f"""
    Based on the following preferences, predict the user's personality type (Introvert, Extrovert, Ambivert, etc.) and briefly explain your reasoning.
    Be concise in your explanation.

    {user_profile}
    """

    headers = {"Content-Type": "application/json"}
    data = {
        "model": OLLAMA_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
        }
    }

    try:
        response = requests.post(OLLAMA_API_BASE_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        result = response.json()
        personality = result.get("response", "No response from model.")
        return personality

    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama server. Please ensure Ollama is running and the model '{OLLAMA_MODEL_NAME}' is downloaded."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err} - {response.text}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        movie = request.form['movie']
        music = request.form['music']
        cartoon = request.form['cartoon']
        hobby = request.form['hobby']
        place = request.form['place']
        timepass = request.form['timepass']

        prediction = predict_personality_ollama(movie, music, cartoon, hobby, place, timepass)

    return render_template('index.html', prediction=prediction)

# --- Run the Flask app ---
if __name__ == '__main__':
    # For development: debug=True for automatic reloading and debugging info
    # For production: set debug=False and use a production-ready WSGI server like Gunicorn
    app.run(debug=True, port=5000) # Runs on http://127.0.0.1:5000/