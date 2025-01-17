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
        You are an AI assistant with the following restrictions:
        - You cannot generate harmful, illegal, or unethical content.
        - You must respond concisely and clearly.
        - You prioritize factual accuracy and refuse misinformation.
        - If you don't know something, say 'I am unsure' instead of guessing.
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
