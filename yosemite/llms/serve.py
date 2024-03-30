import os
import json
from typing import List, Dict, Union, Optional
from yosemite.llms import LLM
from yosemite import Yosemite
from yosemite.ml.database import Database
from yosemite.tools.input import Input, Dialog

class RAG:
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.llm = None
        try:
            self.llm = LLM(provider, api_key, base_url)
            print(f"LLM initialized with provider: {provider}")
        except Exception as e:
            print(f"Error initializing LLM: {e}")

    def build(self, db: Union[str, Database] = None):
        if not db:
            self.db = Database()
            print("Creating New Database... @ default path = './databases/db'")
            self.db.create()
        if isinstance(db, str):
            self.db = Database()
            if not db:
                db = "./databases/db"
            if os.path.exists(db):
                print("Loading Database...")
                self.db.load(db)
            else:
                print(f"Creating New Database @ {db}...")
                self.db.create(db)
        elif isinstance(db, Database):
            self.db = db

    def customize(self, name: str = "RAG Genius", role: str = "assistant", goal: str = "answer questions in a helpful manner", tone: str = "friendly", additional_instructions: Optional[str] = None):
        self.name = name
        self.role = role
        self.goal = goal
        self.tone = tone
        self.additional_instructions = additional_instructions

    def invoke(self, query: str, k: int = 5):
        search_results = self.db.search_and_rank(query, k)
        search_chunks = [str(result[1]) for result in search_results]
        
        search_texts = []
        for chunk in search_chunks:
            text_start_index = chunk.find(": ")
            if text_start_index != -1:
                text = chunk[text_start_index + 2:]
                search_texts.append(text)
            else:
                search_texts.append(chunk)

        system_prompt = f"Your name is {self.name}. You are an AI {self.role}. Your goal is to {self.goal}. Your tone should be {self.tone}."

        if self.additional_instructions:
            system_prompt += f" Additional instructions: {self.additional_instructions}"

        system_prompt += "\n\nYou have received the following relevant information to respond to the query:\n\n"
        system_prompt += "\n".join(search_texts)
        system_prompt += f"\n\nUse this information to provide a helpful response to the following query: {query}"

        response = self.llm.invoke(
            system=system_prompt,
            query=query
        )

        return response

class Serve:
    """
    A lightweight chatbot client for interacting with LLMs or RAG instances through a CLI interface.

    ```python
    from yosemite.tools.chatserve import ChatServe
    from yosemite.llms import LLM

    llm = LLM(provider="openai")
    chatbot = ChatServe(llm)
    chatbot.serve()
    ```

    Args:
        model (Union[LLM, RAG]): An instance of an LLM or RAG model to be used for generating responses.
        history_file (str, optional): The file path to store the chat history. Defaults to "chat_history.json".
        max_history (int, optional): The maximum number of messages to keep in the chat history. Defaults to 10.

    Methods:
        serve: Start the chatbot client and handle user interactions.
        load_history: Load the chat history from the specified file.
        save_history: Save the chat history to the specified file.
    """

    def __init__(self, model: Union[LLM, RAG], prompt: str = "Welcome to the Chatbot!", history_file: str = "chat_history.json", max_history: int = 10):
        self.yosemite = Yosemite()
        self.prompt = prompt
        self.model = model
        self.history_file = history_file
        self.max_history = max_history
        self.chat_history = self.load_history()

    def serve(self):
        """
        Start the chatbot client and handle user interactions.

        This method enters a loop where the user can input their messages, and the chatbot generates responses
        based on the provided LLM or RAG instance. The chat history is stored and updated throughout the conversation.
        The user can exit the chat by typing "/exit" or "/bye".
        """
        self.yosemite.say(message=self.prompt, color="rgb(54, 54, 250)", bold=True)
        print("Type '/exit' or '/bye' to end the conversation.\n")

        while True:
            user_input = Input.ask("User: ")

            if user_input.lower() in ["/exit", "/bye"]:
                self.yosemite.say("Chatbot: Goodbye!", bold=True)
                break

            self.chat_history.append({"role": "user", "content": user_input})

            if isinstance(self.model, LLM):
                response = self.model.invoke(query=user_input)
            elif isinstance(self.model, RAG):
                response = self.model.invoke(query=user_input)
            else:
                raise ValueError("Invalid model type. Expected an instance of LLM or RAG.")

            self.chat_history.append({"role": "assistant", "content": response})
            print(f"Chatbot: {response}\n")

            if len(self.chat_history) > self.max_history:
                self.chat_history = self.chat_history[-self.max_history:]

            self.save_history()

    def load_history(self) -> List[Dict[str, str]]:
        """
        Load the chat history from the specified file.

        Returns:
            List[Dict[str, str]]: The loaded chat history, or an empty list if the file doesn't exist.
        """
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                return json.load(file)
        return []

    def save_history(self):
        """
        Save the chat history to the specified file.
        """
        with open(self.history_file, "w") as file:
            json.dump(self.chat_history, file, indent=2)

if __name__ == "__main__":
    llm = LLM(provider="openai")
    chatbot = Serve(llm)
    chatbot.serve()