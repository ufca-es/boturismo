class ChatBot:
    def __init__(self, responses: dict):
        self.responses = responses

    def get_response(self, user_input: str) -> str:
        user_input = user_input.lower().strip()
        return self.responses.get(user_input, "Desculpe, não entendi o que você quis dizer.")
    
    