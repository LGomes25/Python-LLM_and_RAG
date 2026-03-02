import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from src.config import get_langchain_model

# Iniciando o llm
llm = get_langchain_model()

# Iniciando contador de Iterações
if "count" not in st.session_state:
    st.session_state["count"] = 0

# Iniciando o histórico
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Configurando pagina
st.title("Chatbot com Memória - Aula2")
user_input = st.text_input("Digite sua pergunta: ")
send = st.button("Enviar")


# Botão para limpar histórico
clear = st.button("Limpar Histórico")
if clear:
    st.session_state["chat_history"] = []
    st.session_state["count"] = 0
    st.write("Histórico Limpo!")


# Preparando a resposta
if send and user_input:
    # incrementando contador
    st.session_state["count"] += 1

    # Adicionando a mensagem ao histórico
    st.session_state["chat_history"].append(HumanMessage(content=user_input))

    # Enviando o prompt com histórico
    response = llm.invoke(st.session_state["chat_history"])

    # Armazena a resposta do modelo
    st.session_state["chat_history"].append(AIMessage(content=response.content))

    # Exibe resposta
    st.write(f"Iteração [{st.session_state["count"]}]: {response.content}")
