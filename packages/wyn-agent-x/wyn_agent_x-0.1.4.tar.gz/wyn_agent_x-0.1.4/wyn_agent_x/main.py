import os
from wyn_agent_x.helper import ChatBot, intent_processor, resolve_and_execute, load_metadata
import wyn_agent_x.list_of_apis  # This will ensure that the API functions are registered
import json

# Load metadata
metadata_filepath = os.path.join(os.path.dirname(__file__), 'metadata.json')
metadata = load_metadata(metadata_filepath)

class AgentX:
    def __init__(self, api_key: str, account_sid: str, auth_token: str, protocol: str = "You are a helpful agent."):
        self.event_stream = []
        self.bot = ChatBot(protocol=protocol, api_key=api_key)
        self.account_sid = account_sid
        self.auth_token = auth_token

    def start_chat(self):
        # Friendly welcome message with emoji
        print("👋 Welcome! Press 'EXIT' to quit the chat at any time.")

        prompt = input("User: ")

        while "EXIT" not in prompt:
            # Add user message to event_stream
            self.event_stream.append({"event": "user_message", "content": prompt})
            
            # Process the intent and detect any API calls
            intent_processor(self.event_stream, metadata, self.bot)

            # Check if we need to resolve and execute any API calls
            resolve_and_execute(self.event_stream, metadata, self.account_sid, self.auth_token)

            # Get the next user input
            prompt = input("User: ")

        # Exit message with emoji when the user quits
        print("👋 Thanks for chatting! Have a great day! 🌟")
