from flask import Flask, request, jsonify, render_template
import logging
from flask_cors import CORS
from together import Together

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

logging.basicConfig(level=logging.INFO)

client = Together(api_key="tgp_v1_63eW4lwf6uzNh1IzlqUTwdCEJqHONGGK1a6PHxm6MDE")
model="lgai/exaone-deep-32b"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_input = data.get("message")
        if not user_input:
            return jsonify({"response": "No input received!"})

        # System prompt to restrict AI's behavior
        system_prompt = (
            "You are an expert assistant. "
            "You are designed to answer questions related to medical devices only."
            "Summerize the answer in 2-3 sentences to with word to easy understand."
            "If the question is not about medical device, politely reply that you can only answer medical device questions."
            "My name Chamreoun Boren from Cambodia who develop this AI assistant"
            "Cambodia is a country in Southeast Asia, located on the Indochinese Peninsula that export medical devices."
        )
        response = client.chat.completions.create(
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        ai_reply = response.choices[0].message.content

        return jsonify({"response": ai_reply})
    except Exception as e:
        logging.error(f"Error handling request: {e}")
        return jsonify({"response": "Something went wrong!"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)