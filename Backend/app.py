from flask import Flask, request, jsonify
from flask_cors import CORS
from chat import chat

app = Flask(__name__)
CORS(app) 

@app.route('/question', methods=['POST'])
def ask_question():

    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = chat(question)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
