import vosk
import sounddevice as sd
import json
from service.ai_agent import OpenAIAssistant
from service.system_controller import SystemController

class VoiceAssistant:
    """
    Handles voice commands using Vosk (offline speech recognition).
    """

    def __init__(self, model_path="vosk_model"):
        """
        Initializes Vosk model and AI/system controllers.
        """
        print("🔄 Loading Vosk Model...")
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)  # 16kHz sample rate
        self.ai = OpenAIAssistant(model="gpt-4o-mini")
        self.system = SystemController()

    def listen(self):
        """
        Captures microphone input and converts it to text using Vosk.
        """
        print("🎤 Say something...")

        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                               channels=1, callback=self.callback):
            self.recognizer.Reset()
            while True:
                if self.recognizer.AcceptWaveform():
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print(f"🗣️ Recognized: {text}")
                        return text.lower()

    def callback(self, indata, frames, time, status):
        """
        Audio input callback function for Vosk.
        """
        if status:
            print("⚠️ Audio Input Error:", status)
        self.recognizer.AcceptWaveform(indata)

    def process_voice_command(self):
        """
        Processes recognized voice input and determines the appropriate action.
        """
        command = self.listen()
        if not command:
            return

        # System Commands
        if "open" in command:
            app_name = command.replace("open", "").strip()
            response = self.system.open_application(app_name)
        elif "spotify" in command:
            spotify_command = command.replace("spotify", "").strip()
            response = self.system.control_spotify(spotify_command)
        elif "wiki" in command:
            topic = command.replace("wiki", "").strip()
            response = self.ai.query(f"Summarize the following content from Wikipedia: {topic}")
        else:
            response = self.ai.query(command)

        print(f"🤖 AI Response: {response}")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    while True:
        print("🎙️ Say a command (or 'exit' to quit)...")
        assistant.process_voice_command()
