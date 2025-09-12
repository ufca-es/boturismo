def inicializar_bot_cidade(responses, personality = ""):
    print(f"Bot: Escolha essas opções: {', '.join(responses.keys())}")
    user_input = input("Você: ")
    city = user_input.strip().lower()
    while city not in list(responses.keys()):
        print("Bot: Cidade inválida. Tente novamente.")
        user_input = input("Você: ")
        city = user_input.strip().lower()
    print(f"Bot ({personality}): Olá! Como posso ajudar você com informações sobre {city.title()}?")
        
    return city

def inicializar_bot_personalididade(responses, city): 
    personalities = list(responses[city].keys())
    print(f"Bot: Escolha essas opções de interação: ", ', '.join(personalities))
    user_input = input("Você: ")
    personality = user_input.strip().lower()
    while personality not in personalities:
        print("Bot: Personalidade inválida. Tente novamente.")
        user_input = input("Você: ")
        personality = user_input.strip().lower()
    print(f"Bot ({personality}): Olá! Como posso ajudar você com informações sobre {city.title()}?")
    return personality

    # Armazenamento do histórico de conversas
def armazenar_historico(user_input, bot_response, history_file):
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(f"Você: {user_input}\n")
        f.write(f"Bot: {bot_response}\n")
        
    # Função para exibir o histórico de conversas

def ultimas_interacoes(history_file, n=5):
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        ultimas = linhas[-n:]
        print("-"*15)
        print("Últimas interações:")
        for linha in ultimas:
            print(linha.strip())
        print("-"*15)
        

    except FileNotFoundError:
        print("Nenhum histórico encontrado.")

import os
import json

def salvar_resposta_nova(cidade, personalidade, pergunta, resposta):
    """
    Salva a resposta ensinada pelo usuário no arquivo de aprendizado.
    Cria o arquivo se não existir.
    """
    arquivo = "data/aprendizado.json"

    # Cria o arquivo se não existir
    if not os.path.exists(arquivo):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2, ensure_ascii=False)

    # Carrega o arquivo
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Garante que cidade e personalidade existam
    if cidade not in dados:
        dados[cidade] = {}
    if personalidade not in dados[cidade]:
        dados[cidade][personalidade] = []

    # Adiciona a nova pergunta/resposta
    dados[cidade][personalidade].append({
        "perguntas": [pergunta.lower()],
        "resposta": resposta
    })

    # Salva de volta no JSON
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    print(f"🤖 Aprendi a responder '{pergunta}' com '{resposta}'!")
