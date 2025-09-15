import json

class ResponseLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def load_responses(self) -> dict:
        with open(self.filepath, "r", encoding="utf-8") as file:
            return json.load(file)