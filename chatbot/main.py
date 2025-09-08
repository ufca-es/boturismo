from loader import ResponseLoader
from bot import ChatBot
import os

city = ""
personalities = ""

def main():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "data/responses.json")

    loader = ResponseLoader(file_path)
    responses = loader.load_responses()
    
    bot = ChatBot(responses)
    
    print("Bot iniciado! Digite 'sair' para encerrar.")
    print(f"Bot: Escolha essas opções: {', '.join(responses.keys())}")
    user_input = input("Você: ")
    city = user_input.strip().lower()

    personalities = list(responses[city].keys())
    print(f"Bot: Escolha essas opções de interação: ", ', '.join(personalities))
    user_input = input("Você: ")
    personality = user_input.strip().lower()
    print(f"Bot ({personality}): Olá! Como posso ajudar você com informações sobre {city.title()}?")

    while True:
        user_input = input("Você: ")
        if user_input.lower().strip() == "sair":
            print("Bot: Até mais! 👋")
            break
        response = None

        for item in responses[city][personality]:
            if any(q in user_input.lower() for q in item["perguntas"]):
                response = item["resposta"]
                break

        if response:
            print(f"Bot ({personality}): {response}")
        
if __name__ == "__main__":
    main()

