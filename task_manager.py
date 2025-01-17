import subprocess
import os

class TaskManager:
    def set_reminder(self, reminder_text, time_str):
        """Creates a reminder in macOS Reminders app."""
        try:
            script = f'''
            tell application "Reminders"
                set newReminder to make new reminder
                set name of newReminder to "{reminder_text}"
                set due date of newReminder to date "{time_str}"
            end tell
            '''
            subprocess.run(["osascript", "-e", script])
            return f"✅ Reminder added: '{reminder_text}' at {time_str}"
        except Exception as e:
            return f"❌ Failed to create reminder: {str(e)}"
        
    
    def read_macos_mail(self):
        """Fetches unread emails from the macOS Mail app."""
        try:
            script = '''
            tell application "Mail"
                set unreadMessages to (messages of inbox whose read status is false)
                set emailList to {}
                repeat with msg in unreadMessages
                    set senderName to sender of msg
                    set emailSubject to subject of msg
                    set end of emailList to (senderName & ": " & emailSubject)
                end repeat
                return emailList
            end tell
            '''
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            email_output = result.stdout.strip().split(", ")
            return "\n".join(email_output) if email_output else "📭 No unread emails."
        except Exception as e:
            return f"❌ Error reading macOS Mail: {str(e)}"
        
    
    def search_files(self, filename):
        """Searches for a file by name."""
        for root, _, files in os.walk(os.path.expanduser("~")):
            if filename in files:
                return f"📂 File found: {os.path.join(root, filename)}"
        return f"❌ File '{filename}' not found."
