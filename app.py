from flask import Flask, render_template, request, jsonify, send_file
import os
from gtts import gTTS
import wikipediaapi
import vosk
import sounddevice as sd
import json
import queue
from ai_agent import OpenAIAgent
from system_controller import SystemController
from task_manager import TaskManager
import system_monitor
import re

# Flask Initialization
app = Flask(__name__)

# Initialize AI Agent & System Controller
new_ai_agent = OpenAIAgent(model="gpt-4o-mini")
system_controller = SystemController()
task_manager = TaskManager()

# Wikipedia API Setup
user_agent = "GPT2ChatApp/1.0 based on Python wikipedia-api library"
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=user_agent
)

# Vosk Model Setup
vosk_model = vosk.Model("vosk_model")
audio_queue = queue.Queue()

def get_wiki_content(topic):
    """Fetches Wikipedia content."""
    page = wiki_wiki.page(topic)
    return page.text if page.exists() else "Page not found."

def strip_html_tags(text):
    """Removes HTML tags from the given text."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def generate_speech(text, filename="output.mp3"):
    """Generates speech using gTTS and saves as an audio file."""
    try:
        clean_text = strip_html_tags(text)
        tts = gTTS(text=clean_text, lang="en")
        file_path = os.path.join("static", filename)
        tts.save(file_path)
        return file_path  # Return file path to send to frontend
    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        return None

@app.route('/')
def index():
    """Renders chat interface."""
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    """Processes user text input or transcribed voice commands."""
    try:
        user_input = request.form['text'].strip()

        # Handle Wikipedia Command
        if user_input.startswith('/wiki '):
            topic = user_input[6:].strip()
            wiki_content = get_wiki_content(topic)
            response_text = new_ai_agent.query(f"Summarize the following content: {wiki_content}") if wiki_content != "Page not found." else "Error: Wikipedia page not found."

        # Handle System Open Command
        elif user_input.startswith('/open '):
            app_name = user_input[6:].strip()
            response_text = system_controller.open_application(app_name)

        # Handle Spotify Command
        elif user_input.startswith('/spotify '):
            parts = user_input.split(" ", 2)
            command = parts[1] if len(parts) > 1 else None
            song_name = parts[2] if len(parts) > 2 else None
            response_text = system_controller.control_spotify(command, song_name)

        # Handle macOS Reminder
        elif user_input.startswith("/remind "):
            parts = user_input.replace("/remind ", "").split(" at ")
            if len(parts) == 2:
                response_text = task_manager.set_reminder(parts[0], parts[1])
            else:
                response_text = "❌ Invalid reminder format. Use: /remind <task> at YYYY-MM-DD HH:MM:SS"

        # Handle File Search
        elif user_input.startswith("/search "):
            filename = user_input[8:].strip()
            response_text = task_manager.search_files(filename)

        # Handle macOS Mail
        elif user_input.startswith("/email inbox"):
            response_text = task_manager.read_macos_mail()

        # Default AI Processing
        else:
            response_text = new_ai_agent.query(user_input)

        # Generate speech for the response
        speech_file = generate_speech(response_text)

        return jsonify(message=response_text, audio_url=speech_file if speech_file else None)

    except Exception as e:
        print("Error processing request:", str(e))
        return jsonify(message="An error occurred. Please try again.", audio_url=None)

@app.route('/static/<filename>')
def serve_audio(filename):
    """Serves the generated audio file."""
    return send_file(os.path.join("static", filename))

@app.route('/get_system_stats', methods=['GET'])
def get_system_stats():
    """ Fetch system resource stats and return JSON response. """
    stats = system_monitor.get_system_stats()
    return jsonify(stats)


if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")  # Ensure 'static' folder exists for audio files
    app.run(debug=True)
