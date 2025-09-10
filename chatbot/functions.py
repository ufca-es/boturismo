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
