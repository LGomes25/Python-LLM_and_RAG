import streamlit as st
from chatbot_graph import RAGState, app
from langchain_core.messages import AIMessage, HumanMessage

# Config da pagina
st.set_page_config(layout="wide", page_title="Chatbot com RAG de pdf", page_icon="🗃️")

# Título do chat na tela
st.title("RAG de pdf - Assistente Virtual")

with st.sidebar:
    st.header("Configurações")
    st.write("LLM: meta-llama-3.1-8b-instruct")
    st.write("Embeddings: HuggingFace")
    k = st.slider("Top-k (Documentos recuperados)", 2, 10, 4)
    if st.button("Recarregar retriever"):
        st.cache_resource.clear()

# Verifica se existe mensagem prévia e adiciona boas vindas
if "message_history" not in st.session_state:
    st.session_state["message_history"] = [
        AIMessage(
            content="""Olá! 🗃️ Pergunte algo que esteja dentro dos seus documentos de referência.🗃️"""
        )
    ]

# Entrada do usuário
user_input = st.chat_input("Digite sua pergunta aqui...")

# render histórico
for n in st.session_state["message_history"]:
    role = "assistant" if isinstance(n, AIMessage) else "user"
    with st.chat_message(role):
        st.write(n.content)

# pipeline on submit
if user_input:
    st.session_state["message_history"].append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Buscando nas fontes e gerando resposta..."):
            # Roda o Grapho
            # Passa o histórico e a pergunta atual
            state_in: RAGState = {
                "question": user_input,
                "messages": st.session_state["message_history"],
                "docs": None,
                "context": None,
                "answer": None,
            }
            state_out = app.invoke(state_in)

            answer = state_out.get("answer", "(sem resposta)")
            st.write(answer)

            # Exibe fontes
            docs_used = state_out.get("docs") or []
            if docs_used:
                st.markdown("---")
                st.markdown("🔎 Fontes Utilizadas")
                for i, d in enumerate(docs_used, 1):
                    src = d.metadata.get("source", "desconhecido")
                    page = (
                        f"(p.{d.metadata.get('page')})"
                        if d.metadata.get("page")
                        else ""
                    )
                    with st.expander(f"[{i}] {src}{page}"):
                        st.write(d.page_content)

    # atualiza histórico com a ultima resposta(node_generate já adiciona AIMessage via add_message)
    st.session_state["message_history"] = state_out["messages"]
