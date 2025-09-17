# app.py
import streamlit as st
import os
import random
import json
import time
from functions import gerar_relatorio # Importe a nova função

# --- FUNÇÕES AUXILIARES (do arquivo functions.py) ---
def carregar_respostas_base(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.error(f"Arquivo de respostas não encontrado ou corrompido: {file_path}")
        return {}

def armazenar_historico(pergunta, resposta, history_file, personalidade, cidade):
    try:
        with open(history_file, "a", encoding="utf-8") as f:
            f.write(f"{pergunta.strip()}|{personalidade}|{cidade}\n")
            f.write(f"{resposta.strip()}\n")
    except Exception as e:
        st.error(f"Erro ao salvar histórico: {e}")

def obter_resposta_bot(pergunta_usuario, respostas_disponiveis):
    pergunta_usuario = pergunta_usuario.lower().strip()
    for item in respostas_disponiveis:
        if any(q in pergunta_usuario for q in item.get("perguntas", [])):
            respostas = item.get("respostas", [])
            if respostas:
                return random.choice(respostas)
    return None

# --- CONFIGURAÇÃO INICIAL DA PÁGINA E CAMINHOS ---
st.set_page_config(page_title="Boturismo", page_icon="🐦", layout="wide")

base_path = os.path.dirname(__file__)
pasta_data = os.path.join(base_path, "data")
os.makedirs(pasta_data, exist_ok=True)
file_path_base = os.path.join(pasta_data, "responses.json")

# --- CARREGAMENTO DE DADOS ---
todas_respostas = carregar_respostas_base(file_path_base)
if not todas_respostas:
    st.stop()

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "cidade" not in st.session_state:
    st.session_state.cidade = None
if "personalidade" not in st.session_state:
    st.session_state.personalidade = None
if "history_file" not in st.session_state:
    st.session_state.history_file = ""

# --- BARRA LATERAL (SIDEBAR) PARA CONFIGURAÇÕES ---
with st.sidebar:
    st.title("⚙️ Configurações do ChatBot")
    st.markdown("Configure o bot para começar a conversar.")

    user_name = st.text_input("Seu nome de usuário:", value="visitante")
    if user_name:
        pasta_usuario = os.path.join(pasta_data, f"chat_history_{user_name}")
        os.makedirs(pasta_usuario, exist_ok=True)
        st.session_state.history_file = os.path.join(pasta_usuario, "chat_history.txt")

    cidades_disponiveis = list(todas_respostas.keys())
    st.session_state.cidade = st.selectbox("Escolha a cidade:", cidades_disponiveis)

    if st.session_state.cidade:
        personalidades_disponiveis = list(todas_respostas[st.session_state.cidade].keys())
        st.session_state.personalidade = st.selectbox("Escolha a personalidade:", personalidades_disponiveis)
    
    st.divider()
    
    # --- LÓGICA DO RELATÓRIO ---
    if st.button("📊 Gerar Relatório"):
        if os.path.exists(st.session_state.history_file):
            # Chama a função que agora RETORNA o texto do relatório
            relatorio_texto = gerar_relatorio(st.session_state.history_file)
            # Salva o texto no estado da sessão para ser exibido na tela principal
            st.session_state.relatorio_gerado = relatorio_texto
        else:
            st.warning("Nenhum histórico encontrado para este usuário.")

# --- TELA PRINCIPAL DO CHAT ---
st.title(f"🐦Boturismo: {st.session_state.cidade.title() if st.session_state.cidade else ''}")
st.markdown(f"Interagindo com a personalidade: **{st.session_state.personalidade}**")

# --- Exibição do Relatório (se existir no estado da sessão) ---
if "relatorio_gerado" in st.session_state:
    st.subheader("📈 Relatório de Interações")
    st.text_area("Relatório:", st.session_state.relatorio_gerado, height=250)
    # Limpa o relatório do estado da sessão para que ele não apareça novamente
    del st.session_state.relatorio_gerado

# Exibe o histórico do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Lógica de interação do chat
if prompt := st.chat_input(f"Pergunte sobre {st.session_state.cidade}..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            time.sleep(0.5)
            respostas_disponiveis = todas_respostas[st.session_state.cidade][st.session_state.personalidade]
            resposta_bot = obter_resposta_bot(prompt, respostas_disponiveis)

            if not resposta_bot:
                resposta_bot = "Desculpe, não sei a resposta para isso."
            st.markdown(resposta_bot)

    st.session_state.messages.append({"role": "assistant", "content": resposta_bot})

    armazenar_historico(
        prompt, 
        resposta_bot, 
        st.session_state.history_file, 
        st.session_state.personalidade, 
        st.session_state.cidade
    )

