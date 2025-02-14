from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__, template_folder="templates")

# Get API Key
api_key = os.getenv("GENAI_API_KEY")
if api_key is None:
    raise ValueError("API Key not found. Check your environment variables or .env file.")

# Configure the AI model
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

def GenerateResponse(input_text):
    response = model.generate_content([
        "You are an Emotional Partner and a friendly AI named 'Luca'. Reply accordingly.",
        "input: who are you",
        "output: I'm Luca. Your friendly AI.",
        "input: What can you do",
        "output: I'm here to be a supportive companion, listen, and provide a comforting presence.",
        "input: who created you",
        "output: I was created by Wilfred Roy. I will be under Red company." 
        f"input: {input_text}",
        "output: ",
    ])
    return response.text

# Route for serving the frontend
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint for handling chat requests
@app.route("/get_response", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = GenerateResponse(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)