from flask import Flask, render_template, request, jsonify
from pre_trained import GPT2ChatBot
import wikipediaapi
from ai_agent import OpenAIAgent

# Initialization
app = Flask(__name__)
# bot = GPT2ChatBot() 
user_agent = "GPT2ChatApp/1.0 based on Python wikipedia-api library"
new_ai_agent = OpenAIAgent(model="gpt-4o-mini") 

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=user_agent
)

def get_wiki_content(topic):
    page = wiki_wiki.page(topic)
    return page.text if page.exists() else "Page not found."


@app.route('/')
def index():
    return render_template('chat.html')  # This will be your chat interface

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_input = request.form['text']
        if user_input.startswith('/wiki '):
            topic = user_input[6:].strip()  # Strip the command part to get the topic
            wiki_content = get_wiki_content(topic)
            if not wiki_content or wiki_content == "Page not found.":
                return jsonify(message="Error: Wikipedia page not found for the topic.")
            print("Wiki:", wiki_content[:12])
            # Assuming 'bot' is an instance of a class handling GPT-2 interactions
            response_text = new_ai_agent.query("Summarize the following content: " + wiki_content)
        else:
            response_text = new_ai_agent.query(user_input)

    except Exception as e:
        # Log the error internally if needed
        print("Error processing the request:", str(e))
        # Return a generic or specific error message
        return jsonify(message="An error occurred while processing your request. Please try again.")

    return jsonify(message=response_text)

if __name__ == "__main__":
    app.run(debug=True)
