import subprocess
import os
from datetime import datetime

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
        """Fetches unread emails from the macOS Mail app and summarizes them."""
        try:
            # AppleScript to get unread emails
            script = '''
            tell application "Mail"
                set unreadMessages to (messages of inbox whose read status is false)
                set totalUnread to count of unreadMessages
                set todayCount to 0
                set todayList to {}

                repeat with msg in unreadMessages
                    set senderName to sender of msg
                    set emailSubject to subject of msg
                    set emailDate to date received of msg

                    set formattedDate to (year of emailDate as string) & "-" & (month of emailDate as number as string) & "-" & (day of emailDate as string)
                    set currentDate to (year of (current date) as string) & "-" & (month of (current date) as number as string) & "-" & (day of (current date) as string)

                    if formattedDate is equal to currentDate then
                        set todayCount to todayCount + 1
                        set end of todayList to (senderName & ": " & emailSubject)
                    end if
                end repeat
                
                return totalUnread & "##" & todayCount & "##" & todayList
            end tell
            '''

            # Run the AppleScript and capture the output
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            output = result.stdout.strip().split("##")  # Split the returned values

            if len(output) < 3:
                return "❌ Error processing emails."

            total_unread = output[0]
            today_count = output[1]
            today_emails = output[2].split(", ") if output[2] else []

            # Format the response
            response = f"📧 You have {total_unread} unread emails."
            response += f"\n📅 {today_count} new emails received today."
            if today_count != "0":
                response += "\n📩 Today's emails:\n" + "\n".join(today_emails)

            return response.strip()

        except Exception as e:
            return f"❌ Error reading macOS Mail: {str(e)}"
        
    
    def search_files(self, filename):
        """Searches for a file by name."""
        for root, _, files in os.walk(os.path.expanduser("~")):
            if filename in files:
                return f"📂 File found: {os.path.join(root, filename)}"
        return f"❌ File '{filename}' not found."
