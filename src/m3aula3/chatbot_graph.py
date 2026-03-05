from pathlib import Path
from typing import List, Optional, TypedDict

import streamlit as st
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.graph import StateGraph

from src.config import get_langchain_model
from src.m3aula3.rag_pipeline import build_chroma, load_docs, split_docs

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CHROMA_DIR = BASE_DIR / "chroma_m3a3"


# ============== State Schema =========================
class RAGState(TypedDict):
    question: str
    messages: List[BaseMessage]  # histórico de conversa
    docs: Optional[List[Document]]  # documentos recuperados
    context: Optional[str]  # contexto concatenado para o prompt
    answer: Optional[str]  # resposta final


# ============== State Schema =========================
@st.cache_resource(show_spinner="Carregando banco vetorial...")
def get_retriever(k: int = 2):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectordb = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name="meus_docs",
    )
    return vectordb.as_retriever(search_type="mmr", search_kwargs={"k": k})


# ============== LLM e Prompta =========================
llm = get_langchain_model()


def get_llm():
    return llm


SYSTEM_PROMPT = """
Vovê é um assistente útil, claro e focado em responder com base nas fontes recuperadas.
- Se as fontes não trouxerem evidÊncias suficientes, explique isso e faça clarificações.
- Cite sempre as fontes utilizadas (arquivos e paginas quando disponíveis).
- Seja conciso e preciso. 
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
        (
            "human",
            "Pergunta: {question}\n\nContexto recuperado:\n{context}\n\nResponda de forma objetiva.",
        ),
    ]
)

chain: Runnable = prompt | llm

# ============== NODES =========================


def node_init_pipeline(state: RAGState) -> RAGState:
    """Verifica se o banco existe, se não cria via pipeline"""
    if not CHROMA_DIR.exists() or not any(CHROMA_DIR.iterdir()):
        print("[INFO] Banco não encontrado, rodando pipeline...")
        docs = load_docs()
        chunks = split_docs(docs)
        build_chroma(chunks)
        print("[INFO] Banco criado com sucesso.")
    else:
        print("[INFO] Banco já existe, usando persistido.")

    # retorna o estado sem alterar nada ainda
    return state


def node_retriever(state: RAGState) -> RAGState:
    """Busca documentos relevantes no ChromaDB"""
    retriever = get_retriever()
    docs = retriever.invoke(state["question"])
    state["docs"] = docs
    return state


def node_augment(state: RAGState) -> RAGState:
    """Concatena contexto dos docs recuperados"""
    docs = state.get("docs") or []
    if docs:
        context = "\n\n".join([d.page_content for d in docs[:2]])
        state["context"] = context[:1500]
    else:
        state["context"] = ""
    return state


def node_generate(state: RAGState) -> RAGState:
    """Gera resposta final usando LLM + prompt"""
    response = chain.invoke(
        {
            "question": state["question"],
            "messages": state["messages"],
            "context": state["context"],
        }
    )
    state["answer"] = response.content
    # adiciona resposta ao histórico
    state["messages"].append(response)
    return state


# ============== Monta Grapho =========================
graph = StateGraph(RAGState)

graph.add_node("InitPipeline", node_init_pipeline)
graph.add_node("Retriever", node_retriever)
graph.add_node("AugmentPrompt", node_augment)
graph.add_node("Generate", node_generate)

graph.set_entry_point("InitPipeline")
graph.add_edge("InitPipeline", "Retriever")
graph.add_edge("Retriever", "AugmentPrompt")
graph.add_edge("AugmentPrompt", "Generate")
graph.set_finish_point("Generate")

app = graph.compile()
