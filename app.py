from flask import Flask, request, jsonify, render_template
from groq import Groq
import os

app = Flask(__name__)

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

try:
    with open("knowledge.txt", "r", encoding="utf-8") as file:
        knowledge = file.read()
except:
    knowledge = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data["message"]
        msg = user_message.lower().strip()

        greetings = ["hi", "hello", "hey", "hii", "helo"]

        if msg in greetings:
            return jsonify({
                "reply": "Hello! 😊 I can help you with Cross Browser Compatibility. Ask me anything related to it."
            })
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are an expert chatbot ONLY for Cross Browser Compatibility.

Rules:
- If question is related → answer properly.
- If NOT related → say:
  "I can only assist with Cross Browser Compatibility topics."

Be polite and friendly.

Knowledge:
{knowledge}
"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
