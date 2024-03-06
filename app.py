from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

openai_api_key = 'YOUR_OPENAI_API_KEY'
openai_headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai_api_key}'
}

conversations = {}

def call_openai_api(prompt):
    data = {
        'model': 'text-davinci-003',  # Update this to GPT-4 model when available
        'prompt': prompt,
        'max_tokens': 50
    }
    response = requests.post('https://api.openai.com/v1/engines/text-davinci-003/completions', headers=openai_headers, json=data)
    return response.json()['choices'][0]['text']

@app.route('/')
def home():
    return render_template('index.html', conversations=conversations)

@app.route('/submit_message', methods=['POST'])
def submit_message():
    message = request.form['message']
    conversation_id = request.form['conversation_id']
    conversations.setdefault(conversation_id, []).append(message)
    if message.strip().lower() != 'exit':
        response = call_openai_api('\n'.join(conversations[conversation_id]))
        conversations[conversation_id].append(response)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
