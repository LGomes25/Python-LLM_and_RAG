import streamlit as st
from chatbot import app
from langchain_core.messages import AIMessage, HumanMessage

# Config da pagina
st.set_page_config(
    layout="wide", page_title="Chatbot de loja de bicicleta", page_icon="🚴"
)

# Título do chat na tela
st.title("Loja de Bicicletas - Assistente Virtual")

# Verifica se existe mensagem prévia e adiciona boas vindas
if "message_history" not in st.session_state:
    st.session_state["message_history"] = [
        AIMessage(
            content="""Olá! 🚴 Sou seu assistente virtual da loja de bicicletas para ajudar você a encontrar informações sobre produtos da loja. Como posso ajudar você?"""
        )
    ]

# Entrada do usuário e chamada a llm
user_input = st.chat_input("Digite aqui...")

if user_input:
    st.session_state["message_history"].append(HumanMessage(content=user_input))

    response = app.invoke({"messages": st.session_state["message_history"]})
    st.session_state["message_history"] = response["messages"]

# Exibição das mensagens
for this_message in st.session_state["message_history"]:
    if isinstance(this_message, AIMessage):
        message_box = st.chat_message("assistant")
    else:
        message_box = st.chat_message("user")
    message_box.markdown(this_message.content)
