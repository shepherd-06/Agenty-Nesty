# 🔥 Agent Nesty! 🔥

## 🚀 Overview

Agent Nesty! is a personal AI assistant that helps automate tasks, fetch information, and control various system functions on macOS. It integrates GPT-4o, Wikipedia search, macOS automation, Spotify control, and text-to-speech (gTTS) to provide a seamless user experience. This app runs as a Flask web app and can also be used as a desktop application via Electron.

## 🔧 Technologies Used

* Python (Flask) – Backend server & AI processing
* OpenAI GPT-4o – AI response generation
* Wikipedia API – Fetching summaries from Wikipedia
* macOS AppleScript – Controlling macOS applications
* Spotify AppleScript – Managing Spotify playback
* gTTS (Google Text-to-Speech) – Converting AI responses into speech
* Vosk – Speech-to-text for voice input (planned feature)
* Electron.js – Packaging into a macOS desktop app

## 🛠 Installation & Setup

* 1️⃣ Clone the Repository
* 2️⃣ Create a Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

* 3️⃣ Set Up .env File

Rename .env.example to .env and fill in the necessary API keys:

```bash
mv .env.example .env
```

Example `.env` file

```text
openai=<EXAMPLE>
```

* 4️⃣ Run the Flask Server

```bash
python app.py
```

Flask should now be running on <http://127.0.0.1:5000>

* 5️⃣ (Optional) Run as a Desktop App (Electron)

```bash
npm install
npm start
```

📌 Features & Commands

* ✅ AI Chatbot with GPT-4o: Ask any question, and Agent Nesty! will generate a response using OpenAI's GPT-4o.
* 📖 Wikipedia Summarization: Use /wiki <topic> to fetch a summary from Wikipedia `Example: /wiki Byzantine Empire`
* 📂 Open macOS Applications: Use /open <app_name> to open an app. `Example: /open safari`
* 🎵 Spotify Control: Use /spotify <command> to control playback. /spotify play, /spotify pause, /spotify next
* 📧 Email Summarization: Use /email inbox to check unread emails from macOS Mail.
* 🔍 File Search: Use /search <filename> to find files on macOS. `Example: /search resume.pdf`
* ⏰ macOS Reminders: Use /remind <task> at <time> to create a reminder. `Example: /remind Meeting at 14:30`
* 🔊 Text-to-Speech (gTTS Integration): AI responses are also spoken aloud using Google Text-to-Speech.

🚀 Enjoy using Agent Nesty! Let us know if you have any feature suggestions! 😃

## Credits

Icon made by [Freepik](https://www.flaticon.com/free-icons/secret-agent "secret-agent icons") from [Flaticon](https://www.flaticon.com/).
