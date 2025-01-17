import subprocess

class SystemController:
    """
    Handles system-level tasks such as opening applications and controlling Spotify playback.
    """

    def open_application(self, app_name):
        """
        Opens an application on the laptop based on the app name.
        """
        try:
            if app_name.lower() == "chrome":
                subprocess.run(["open", "-a", "Google Chrome"])  # macOS
            elif app_name.lower() == "spotify":
                subprocess.run(["open", "-a", "Spotify"])  # macOS
            elif app_name.lower() == "vscode":
                subprocess.run(["code"])  # VS Code (assumes it's in PATH)
            else:
                return f"❌ Unknown application '{app_name}'. Try 'chrome', 'spotify', or 'vscode'."

            return f"✅ Opening {app_name}..."
        except Exception as e:
            return f"❌ Failed to open {app_name}. Error: {str(e)}"

    def is_spotify_running(self):
        """
        Checks if Spotify is currently running.
        """
        try:
            result = subprocess.run(["pgrep", "-x", "Spotify"], capture_output=True, text=True)
            return result.returncode == 0  # Returns True if Spotify is running, False otherwise
        except Exception as e:
            return False

    def control_spotify(self, command, song_name=None):
        """
        Controls Spotify playback. Supports play, pause, next, previous, shuffle, and playing a song.
        """
        if not self.is_spotify_running():
            return "❌ Spotify is not running. Open Spotify first."

        try:
            if command == "play":
                subprocess.run(["osascript", "-e", 'tell application "Spotify" to play'])
                return "▶️ Playing music..."
            elif command == "pause":
                subprocess.run(["osascript", "-e", 'tell application "Spotify" to pause'])
                return "⏸️ Pausing music..."
            # elif command == "next":
            #     subprocess.run(["osascript", "-e", 'tell application "Spotify" to next track'])
            #     return "⏭️ Skipping to next song..."
            # elif command == "previous":
            #     subprocess.run(["osascript", "-e", 'tell application "Spotify" to previous track'])
            #     return "⏮️ Going back to previous song..."
            # elif command == "shuffle":
                # subprocess.run(["osascript", "-e", 'tell application "Spotify" to set shuffling to true'])
                # return "🔀 Shuffle mode activated."
            elif command == "play_song" and song_name:
                apple_script = f'tell application "Spotify" to play track "spotify:track:{song_name}"'
                subprocess.run(["osascript", "-e", apple_script])
                return f"🎵 Playing {song_name}..."
            else:
                return "❌ Invalid Spotify command. Try 'play', 'pause', 'next', 'previous', or 'shuffle'."
        except Exception as e:
            return f"❌ Failed to execute Spotify command. Error: {str(e)}"
