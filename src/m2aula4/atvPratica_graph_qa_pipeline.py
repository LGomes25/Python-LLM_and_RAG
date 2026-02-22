import os
from typing import List, TypedDict

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph

from src.config import get_langchain_model
from src.m2aula4.atvPratica_data_ingestion import retriever


class QAState(TypedDict):
    pergunta: str
    docs: List[Document]
    contexto: str
    resposta: str


# Inicializar modelo
llm = get_langchain_model()

# Prompt
qa_prompt = ChatPromptTemplate.from_template(
    "Você é um assistente amigável que responde perguntas usando apenas o contexto fornecido.\n"
    "Pergunta: {pergunta}\n\n"
    "Contexto:\n{contexto}\n\n"
    "Responda de forma clara e concisa. Se a resposta não estiver no contexto, diga: 'Não encontrei essa informação no contexto'.\n"
    "Inclua a fonte no formato [fonte: título]."
)


# Função auxiliar
def format_docs(docs):
    blocos = []
    for d in docs:
        if "title" in d.metadata and d.metadata["title"]:
            fonte = d.metadata["title"]
        elif "source" in d.metadata:
            fonte = d.metadata["source"]
        elif "file_path" in d.metadata:
            fonte = os.path.basename(d.metadata["file_path"])
        else:
            fonte = "Documento"

        blocos.append(f"[fonte: {fonte}] {d.page_content}")
    return "\n\n***\n\n".join(blocos)


# Nós do grafo
def user_input_node(state: QAState) -> QAState:
    pergunta = input("\nDigite sua pergunta: ")
    state["pergunta"] = pergunta
    return state


def retriever_node(state: QAState) -> QAState:
    docs = retriever.invoke(state["pergunta"])
    state["docs"] = docs
    return state


def context_node(state: QAState) -> QAState:
    contexto = format_docs(state["docs"])
    state["contexto"] = contexto
    return state


def llm_node(state: QAState) -> QAState:
    msg = qa_prompt.format_messages(
        pergunta=state["pergunta"], contexto=state["contexto"]
    )
    out = llm.invoke(msg)
    state["resposta"] = str(out.content)
    print("\nLLM: ", state["resposta"])
    return state


# Construção do grafo
graph = StateGraph(QAState)
graph.add_node("user_input", user_input_node)
graph.add_node("retriever", retriever_node)
graph.add_node("context", context_node)
graph.add_node("llm", llm_node)

graph.set_entry_point("user_input")
graph.add_edge("user_input", "retriever")
graph.add_edge("retriever", "context")
graph.add_edge("context", "llm")
graph.add_edge("llm", END)

# Compilar e executar
app = graph.compile()

# Iniciar o grapho com valores vazios
initial_state: QAState = {"pergunta": "", "docs": [], "contexto": "", "resposta": ""}

app.invoke(initial_state)
