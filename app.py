from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"
API_URL = "https://api.perplexity.ai/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")

    payload = {
        "model": "sonar",  # a valid model per docs
        "messages": [
            {"role": "system", "content": "Be concise and cite sources."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        resp = requests.post(API_URL, headers=HEADERS, json=payload)
        resp.raise_for_status()
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except requests.exceptions.HTTPError as e:
        return jsonify({"reply": f"HTTP Error {resp.status_code}: {resp.text}"})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
