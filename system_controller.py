import subprocess
import os

class SystemController:
    """
    Handles system-level tasks such as opening applications and controlling Spotify playback.
    """

    def find_application(self, app_name):
        """
        Searches for an installed application in the `/Applications` folder.
        Returns the full path if found, otherwise returns None.
        """
        applications_folder = "/Applications"
        possible_apps = [app for app in os.listdir(applications_folder) if app_name.lower() in app.lower()]

        if possible_apps:
            return os.path.join(applications_folder, possible_apps[0])  # Return the first match
        return None

    def open_application(self, app_name):
        """
        Opens an application if it's found, otherwise suggests available options.
        """
        try:
            found_app = self.find_application(app_name)

            if found_app:
                subprocess.run(["open", "-a", found_app])  # Open found application
                return f"Opening {app_name}..."
            else:
                return f"Application '{app_name}' not found. Try specifying a correct app name."

        except Exception as e:
            return f"Failed to open {app_name}. Error: {str(e)}"

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
            return "Spotify is not running. Open Spotify first."

        try:
            if command == "play":
                subprocess.run(["osascript", "-e", 'tell application "Spotify" to play'])
                return "Playing music..."
            elif command == "pause":
                subprocess.run(["osascript", "-e", 'tell application "Spotify" to pause'])
                return "Pausing music..."
            elif command == "next":
                subprocess.run(["osascript", "-e", 'tell application "Spotify" to next track'])
                return "⏭️ Skipping to next song..."
            elif command == "previous":
                subprocess.run(["osascript", "-e", 'tell application "Spotify" to previous track'])
                return "⏮️ Going back to previous song..."
            elif command == "shuffle":
                subprocess.run(["osascript", "-e", 'tell application "Spotify" to set shuffling to true'])
                return "🔀 Shuffle mode activated."
            elif command == "play_song" and song_name:
                apple_script = f'tell application "Spotify" to play track "spotify:track:{song_name}"'
                subprocess.run(["osascript", "-e", apple_script])
                return f"Playing {song_name}..."
            else:
                return "Invalid Spotify command. Try 'play', 'pause', 'next', 'previous', or 'shuffle'."
        except Exception as e:
            return f"Failed to execute Spotify command. Error: {str(e)}"
