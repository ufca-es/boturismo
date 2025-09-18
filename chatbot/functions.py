import os
import json
from collections import Counter

# ---------------------------
# Funções do bot em terminal
# ---------------------------
def inicializar_bot_cidade(responses, personality=""):
    print(f"Bot: Escolha essas opções: {', '.join(responses.keys())}")
    user_input = input("Você: ")
    city = user_input.strip().lower()
    while city not in responses.keys():
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

# ---------------------------
# Histórico
# ---------------------------
def armazenar_historico(pergunta, resposta, history_file, personalidade, cidade):
    """
    Salva pergunta, resposta, personalidade e cidade no histórico.
    """
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(f"{pergunta.strip()}|{personalidade}|{cidade}\n")
        f.write(f"{resposta.strip()}\n")

def ultimas_interacoes(history_file, n=5):
    """
    Retorna as últimas n interações como string formatada.
    """
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            linhas = [linha.strip() for linha in f.readlines() if linha.strip()]

        if not linhas:
            return "Nenhuma interação registrada.\n"

        ultimas = linhas[-(n*2):]  # cada interação = 2 linhas
        resultado = "Últimas interações:\n" + "-"*25 + "\n"
        for i in range(0, len(ultimas), 2):
            resultado += f"{ultimas[i]}\n{ultimas[i+1]}\n"
        resultado += "-"*25
        return resultado
    except FileNotFoundError:
        return "Nenhum histórico encontrado.\n"

# ---------------------------
# Aprendizado
# ---------------------------
def salvar_resposta_nova(cidade, personalidade, pergunta, resposta):
    """
    Salva a resposta ensinada pelo usuário no arquivo de aprendizado.
    """
    arquivo = "data/aprendizado.json"
    if not os.path.exists(arquivo):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2, ensure_ascii=False)

    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    if cidade not in dados:
        dados[cidade] = {}
    if personalidade not in dados[cidade]:
        dados[cidade][personalidade] = []

    dados[cidade][personalidade].append({
        "perguntas": [pergunta.lower()],
        "resposta": resposta
    })

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    print(f"🤖 Aprendi a responder '{pergunta}' com '{resposta}'!")

def carregar_aprendizado():
    """
    Carrega o aprendizado do arquivo JSON.
    """
    arquivo = "data/aprendizado.json"
    if not os.path.exists(arquivo):
        return {}
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------
# Relatórios
# ---------------------------
def gerar_relatorio(history_file):
    """
    Lê o arquivo de histórico, gera um relatório consolidado E RETORNA COMO TEXTO (STRING).
    Não cria mais um arquivo .txt.
    """
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            linhas = [linha.strip() for linha in f.readlines() if linha.strip()]

        if not linhas:
            return "Nenhuma interação registrada para gerar relatório."

        perguntas_com_meta = linhas[::2]
        
        # --- Contagem de perguntas ---
        perguntas_texto = [p.split("|")[0] for p in perguntas_com_meta]
        contador_perguntas = Counter(perguntas_texto)
        
        if not contador_perguntas:
             return "Não foi possível extrair dados de perguntas para o relatório."

        pergunta_frequente, freq = contador_perguntas.most_common(1)[0]

        # --- Contagem de personalidades ---
        personalidades = [p.split("|")[1] for p in perguntas_com_meta if len(p.split("|")) > 1]
        contador_personalidades = Counter(personalidades)
        
        # --- Monta a string do relatório ---
        relatorio_str = (
            f"Relatório de Interações do Chat\n"
            f"-----------------------------------\n"
            f"Total de interações: {len(perguntas_texto)}\n"
            f"Pergunta mais frequente: '{pergunta_frequente}' ({freq} vezes)\n\n"
            f"Uso de personalidades:\n"
        )
        if not contador_personalidades:
            relatorio_str += "- Nenhuma personalidade registrada.\n"
        else:
            for pers, count in contador_personalidades.items():
                relatorio_str += f"- {pers}: {count} vezes\n"
        
        return relatorio_str

    except FileNotFoundError:
        return "Arquivo de histórico não encontrado para gerar o relatório."
    except Exception as e:
        return f"Ocorreu um erro ao gerar o relatório: {e}"

def ultimas_interacoes_relatorio(relatorio_file):
    """
    Lê e retorna o relatório como lista de strings.
    """
    try:
        with open(relatorio_file, "r", encoding="utf-8") as f:
            linhas = [linha for linha in f.readlines()]
            return linhas
    except FileNotFoundError:
        return ["Nenhum relatório encontrado.\n"]

# functions.py

def sugerir_perguntas(caminho_arquivo):
    """
    Lê o histórico de um usuário, encontra as 5 perguntas mais frequentes
    e retorna uma lista com elas.
    """
    from collections import Counter
    cont_perguntas = Counter()
    
    try:
        # Percorre o arquivo e conta as perguntas (linhas ímpares)
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            for i, linha in enumerate(f, start=1):
                if i % 2 != 0:  # Apenas linhas ímpares (perguntas)
                    pergunta = linha.lower().strip()
                    if pergunta:  # Ignora linhas em branco
                        pergunta_chave = pergunta.split("|")[0].strip()
                        cont_perguntas[pergunta_chave] += 1
                        
        # Pega as 5 perguntas mais comuns  
        top5 = cont_perguntas.most_common(5)
        
        # Retorna apenas os textos das perguntas
        return [pergunta for pergunta, _ in top5]
    except FileNotFoundError:
        return [] # Retorna uma lista vazia se o histórico não existir