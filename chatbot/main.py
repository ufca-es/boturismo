from loader import ResponseLoader
from bot import ChatBot
from functions import inicializar_bot_cidade, inicializar_bot_personalididade, armazenar_historico, ultimas_interacoes
import os

city = ""
personalities = ""

def main():
    user_name = str(input("Digite um nome para seu usuário (Válido para outras requisições):"))
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "data/responses.json")
    pasta_data = os.path.join(base_path, "data")
    arquivos = os.listdir(pasta_data)
    pasta_usuario = os.path.join(pasta_data, f"chat_history_{user_name}")
    os.makedirs(pasta_usuario, exist_ok=True)
    nome_arquivo = f"chat_history.txt"
    history_file = os.path.join(pasta_usuario, nome_arquivo)
    
    loader = ResponseLoader(file_path)
    responses = loader.load_responses()
    
    bot = ChatBot(responses)
    if history_file:
        print(ultimas_interacoes(history_file))
    print("Bot iniciado! Digite 'sair' para encerrar.")
    
    city = inicializar_bot_cidade(responses)
    personality = inicializar_bot_personalididade(responses, city)

    while True:
        user_input = input("Você: ")
        if user_input.lower().strip() == "sair":
            print("Bot: Até mais! 👋")
            break
        response = None

        if user_input.lower().strip() == "personalidade":
            personality = inicializar_bot_personalididade(responses, city)
            continue
        
        elif user_input.lower().strip() == "cidade":
            city = inicializar_bot_cidade(responses, personality)
            continue

        for item in responses[city][personality]:
            if any(q in user_input.lower() for q in item["perguntas"]):
                response = item["resposta"]
                break
        
        if response is not None:
            armazenar_historico(user_input, response, history_file)
        
        if response:
            print(f"Bot ({personality}): {response}")
        else:
            print(f"Não há essa resposta no nosso banco!")
            

        
if __name__ == "__main__":
    main()

