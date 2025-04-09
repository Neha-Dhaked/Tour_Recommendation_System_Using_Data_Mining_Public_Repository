# import os
# from flask import Flask, request, jsonify
# from transformers import pipeline
# from flask_cors import CORS  # Allows frontend to talk to backend

# # Disable TensorFlow OneDNN optimizations
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# # Initialize chatbot model
# chatbot = pipeline("text-generation", model="facebook/blenderbot-400M-distill")

# # Create Flask app
# app = Flask(__name__)
# CORS(app)  # Enable Cross-Origin Resource Sharing

# @app.route("/chat", methods=["POST"])
# def chat():
#     try:
#         user_input = request.json.get("message", "")
#         if not user_input:
#             return jsonify({"reply": "Please enter a message."}), 400

#         response = chatbot(user_input)
#         chatbot_reply = response[0]["generated_text"]

#         return jsonify({"reply": chatbot_reply})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)  # Runs on localhost:5000



from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

#  Load DialoGPT-small
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

#  Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@app.route("/", methods=["GET"])
def home():
    return "Chatbot service is running on port 5001. Use /chat to send messages."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "Please enter a message!"})

    #  Encode user input and move to the correct device
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt").to(device)

    #  Generate response with limited length
    response_ids = model.generate(input_ids, max_length=50, pad_token_id=tokenizer.eos_token_id)

    #  Decode response
    bot_reply = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

    return jsonify({"reply": bot_reply})  # Returning JSON response

if __name__ == '__main__':
    app.run(port=5001, debug=True)  #  Running on port 5001
