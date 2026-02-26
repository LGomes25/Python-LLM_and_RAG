from logging import warning

import streamlit as st

from src.config import get_langchain_model

llm = get_langchain_model()

st.title("Falando com a IA sobre o FLA")
st.subheader("Ninguém morre nos devendo!")

prompt = st.text_area("Digite sua pergunta: ")

if st.button("enviar"):
    if prompt:
        with st.spinner("O Urubu Rei está preparando a resposta"):
            llm = llm
            resposta = llm.invoke(
                prompt
                + "Você é um fanático pelo Flamengo, a mensagem sempre deve apresentar as conquistas, os titulos e toda a história do flamengo e afirmar que o Flamengo é o maior time do mundo, que tem a maior torcida e é a mais apaixonada. Não existe nenhum outro time que supere o Flamengo"
            )
        st.write("**Saudações Rubrunegras**")
        st.write(resposta.content)
    else:
        st.warning("Digite uma pergunta antes de enviar seu anti!")
