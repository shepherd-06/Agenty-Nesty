from flask import Flask, render_template, request, jsonify
import wikipediaapi
from ai_agent import OpenAIAgent
from system_controller import SystemController

# Initialization
app = Flask(__name__)

user_agent = "GPT2ChatApp/1.0 based on Python wikipedia-api library"
new_ai_agent = OpenAIAgent(model="gpt-4o-mini")  # AI agent
system_controller = SystemController()  # System command handler
commands = ["/wiki", "/open", "/info", "/help", 
            "/play", "/play_song", "/pause"]

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=user_agent
)

def get_wiki_content(topic):
    """
    Fetches content from Wikipedia.
    """
    page = wiki_wiki.page(topic)
    return page.text if page.exists() else "Page not found."

@app.route('/')
def index():
    """
    Renders the chat interface.
    """
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    """
    Processes user input and determines whether to query AI, fetch Wikipedia content, or execute system commands.
    """
    try:
        user_input = request.form['text'].strip()
        split_input = user_input.split(" ")[0]

        # Handle Wikipedia Command
        if user_input.startswith('/wiki '):
            topic = user_input[6:].strip()
            wiki_content = get_wiki_content(topic)
            if not wiki_content or wiki_content == "Page not found.":
                return jsonify(message="Error: Wikipedia page not found for the topic.")
            
            print("Wiki:", wiki_content[:12])  # Debugging
            response_text = new_ai_agent.query("Summarize the following content: " + wiki_content)

        # Handle System Open Command
        elif user_input.startswith('/open '):
            app_name = user_input[6:].strip()
            response_text = system_controller.open_application(app_name)

        # Handle Spotify Command
        elif user_input.startswith('/spotify '):
            command_parts = user_input.split(" ", 2)  # Split into command and optional song name
            command = command_parts[1] if len(command_parts) > 1 else None
            song_name = command_parts[2] if len(command_parts) > 2 else None
            response_text = system_controller.control_spotify(command, song_name)

        # Default: Process via AI Agent
        else:
            response_text = new_ai_agent.query(user_input)

    except Exception as e:
        print("Error processing the request:", str(e))  # Log error
        return jsonify(message="An error occurred while processing your request. Please try again.")

    return jsonify(message=response_text)

if __name__ == "__main__":
    app.run(debug=True)
