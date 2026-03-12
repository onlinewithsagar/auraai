from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# -------------------------------
# SECURE CONFIGURATION
# -------------------------------
# The app will securely fetch the key from Render's cloud environment
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    chat = model.start_chat(history=[])
else:
    print("⚠️ WARNING: GEMINI_API_KEY environment variable not found.")
    chat = None

# -------------------------------
# ROUTES
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def get_bot_response():
    if not chat:
        return jsonify({"error": "Server missing API Key."}), 500

    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"error": "Empty message"}), 400
        
    try:
        response = chat.send_message(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render assigns a dynamic port automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)