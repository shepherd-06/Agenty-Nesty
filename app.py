from flask import Flask, render_template, request, jsonify
from pre_trained import GPT2ChatBot

app = Flask(__name__)
bot = GPT2ChatBot() 


@app.route('/')
def index():
    return render_template('chat.html')  # This will be your chat interface

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['text']
    response_text = bot.generate_text(user_input)
    return jsonify(message=response_text)

if __name__ == "__main__":
    app.run(debug=True)
