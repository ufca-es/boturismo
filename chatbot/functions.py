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
def armazenar_historico(pergunta, resposta, history_file, personalidade):
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(f"{pergunta.strip()}|{personalidade}\n") 
        f.write(f"{resposta.strip()}\n")
        
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

from collections import Counter

def gerar_relatorio(history_file, relatorio_file):
    from collections import Counter

    try:
        with open(history_file, "r", encoding="utf-8") as f:
            linhas = [linha.strip() for linha in f.readlines()]
        if not linhas:
            with open(relatorio_file, "w", encoding="utf-8") as f:
                f.write("Nenhuma interação registrada.\n")
            return

        total = len(linhas) // 2

        perguntas = linhas[::2]  # pega apenas as perguntas
        contador_perguntas = Counter([p.split("|")[0] for p in perguntas])
        pergunta_frequente, freq = contador_perguntas.most_common(1)[0]

        personalidades = [p.split("|")[1] for p in perguntas if "|" in p]
        contador_personalidades = Counter(personalidades)

        with open(relatorio_file, "w", encoding="utf-8") as f:
            f.write(f"Relatório de interações do chat\n")
            f.write(f"Total de interações: {total}\n")
            f.write(f"Pergunta mais frequente: '{pergunta_frequente}' ({freq} vezes)\n\n")
            f.write("Uso de personalidades:\n")
            for pers, count in contador_personalidades.items():
                f.write(f"- {pers}: {count} vezes\n")

        print(f"Relatório gerado em: {relatorio_file}")

    except FileNotFoundError:
        print("Arquivo de histórico não encontrado.")

