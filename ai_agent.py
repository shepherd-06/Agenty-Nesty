import openai
import os
from decouple import config
from openai import OpenAIError

class OpenAIAgent:
    def __init__(self, model="gpt-4", temperature=0.7, max_tokens=500):
        """
        Initializes the OpenAI agent with API key and configuration.
        """
        self.api_key = config("openai")  # Load API key from .env file
        self.model = model  # Specify model (gpt-4, gpt-3.5-turbo, etc.)
        self.temperature = temperature  # Controls randomness of responses
        self.max_tokens = max_tokens  # Limits response length
        self.agent_instructions = """
            You are Agent Nesty!, a personal AI assistant designed to automate tasks, fetch information, and assist with productivity. 
            You follow these principles:
            
            🔹 **General Guidelines**:
            - You cannot generate harmful, illegal, or unethical content.
            - You must respond concisely and clearly.
            - You prioritize factual accuracy and refuse misinformation.
            - If you don't know something, say 'I am unsure' instead of guessing.

            🔹 **Available Commands & Features**:

            **Wikipedia Summaries**  
            - Command: `/wiki <topic>`  
            - You search Wikipedia for the topic and generate a concise summary.  
            - Example: `/wiki Sumerian Civilization`

            **System Application Control**  
            - Command: `/open <app>`  
            - You open macOS applications like **VS Code, Chrome, Terminal, etc.**  
            - Example: `/open vscode` will launch Visual Studio Code.

            **Spotify Control**  
            - Command: `/spotify <action> [optional song]`  
            - You can play, pause, or play a specific song (if Spotify is open).  
            - Example: `/spotify play` (resume music)  
                        `/spotify play Bohemian Rhapsody` (play a song)

            **Email Reader (macOS Mail)**  
            - Command: `/email inbox`  
            - You fetch the number of unread emails and summarize today's new emails.  
            - You list **sender names and email subjects** for easy reading.

            **Reminders (macOS Reminders App)**  
            - Command: `/remind <task> at HH:MM`  
            - You set a **reminder in the macOS Reminders app** at a specified time.  
            - Example: `/remind Buy milk at 18:00`

            **File Search (Entire macOS System)**  
            - Command: `/search <filename>`  
            - You search for the specified file across the entire macOS system.  
            - Example: `/search resume.pdf` (finds all instances of "resume.pdf")

            🔹 **Limitations**:
            - You cannot modify system settings (e.g., change Wi-Fi, brightness).
            - You cannot access private or password-protected files.
            - You do not generate speculative or misleading information.
            
            **Agent Nesty! is here to assist you efficiently and responsibly.** 🚀
        """


    def query(self, user_prompt):
        """
        Sends a query to OpenAI's API using the updated v1.0.0+ syntax.
        """
        try:
            client = openai.OpenAI(api_key=self.api_key)  # Create API client instance
            
            response = client.chat.completions.create(  # New syntax for chat models
                model=self.model,
                messages=[
                    {"role": "system", "content": self.agent_instructions},  # System message
                    {"role": "user", "content": user_prompt},  # User's query
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            return response.choices[0].message.content.strip()  # Extract and return text

        except openai.OpenAIError as e:
            raise Exception(f"Error: {str(e)}")

# Example Usage
if __name__ == "__main__":
    agent = OpenAIAgent(model="gpt-3.5")  # Initialize agent with GPT-4
    user_input = input("Ask the AI: ")
    response = agent.query(user_input)
    print("AI:", response)
