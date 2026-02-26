from logging import warning

import streamlit as st

from src.config import get_langchain_model

# Chamada a LLM
llm = get_langchain_model()

# Título do chat na tela
st.title("Chat com IA usando LangChain")

# Título do campo de entrada do usuário
prompt = st.text_area("Digite sua pergunta: ")

# Botão de envio: dispara a chamada ao modelo, concatena instruções adicionais à pergunta e exibe a resposta; se o campo estiver vazio, mostra aviso.
if st.button("enviar"):
    if prompt:
        llm = llm
        resposta = llm.invoke(
            prompt
            + "A mensagem deve conter algo sobre a criação do GPT2 e 3, indo até tempos mais recentes, ainda destacando preocupações éticas em relação ao uso das ferramentas."
        )
        st.write("**Resposta**", resposta.content)
    else:
        st.warning("Digite uma pergunta antes de enviar.")
