import json
import os

CHAT_HISTORY_FILE = "chat_history.json"

class ChatHistory:
    def __init__(self):
        """Initialize ChatHistory by loading existing history from the JSON file."""
        self.history = self._load_history()

    def _load_history(self):
        """Load chat history from the JSON file."""
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, "r") as file:
                return json.load(file)
        return []

    def _save_history(self):
        """Save chat history to the JSON file."""
        with open(CHAT_HISTORY_FILE, "w") as file:
            json.dump(self.history, file, indent=4)

    def add_entry(self, question, answer):
        """Add a new question-answer pair to the history and save it."""
        self.history.append({"question": question, "answer": answer})
        self._save_history()

    def get_history(self):
        """Retrieve the chat history."""
        return self.history

    def clear_history(self):
        """Clear the chat history both in memory and in the JSON file."""
        self.history = []
        self._save_history()
