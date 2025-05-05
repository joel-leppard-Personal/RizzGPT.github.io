from flask import Flask, request, jsonify
from gpt4all import GPT4All
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Or a specific domain

model = GPT4All("Llama-3.2-3B-Instruct-Q4_0.gguf")  # Ensure this is the right path

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    system_message = " provide concise summaries of the topic in NO MORE THAN 50 WORDS. Avoid unnecessary details or long explanations."

    user_prompt = data.get("prompt", "")

    # Clear, forceful instruction to answer in no more than 50 words
    modified_prompt = (f"the topic is between the commas: '{user_prompt}'\nDO NOT WRITE MORE THAN 50 WORDS.")

    final_prompt = f"{system_message}\n{modified_prompt}"
    # Generate the model's response
    print(final_prompt)
    response = model.generate(final_prompt, max_tokens=150)

    # Manually trim the response to 50 words
    response_words = response.strip().split()[:80]  # Slice the response to the first 50 words
    response = ' '.join(response_words)

    return jsonify({"response": response})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
