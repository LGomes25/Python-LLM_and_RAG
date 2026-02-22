import os

from langchain_core.prompts import ChatPromptTemplate
from rich import print

from src.config import get_langchain_model
from src.m2aula4.atvPratica_data_ingestion import retriever

# 1. Inicializar modelo de linguagem
llm = get_langchain_model()

# 2. Definir prompt de QA
qa_prompt = ChatPromptTemplate.from_template(
    "Você é um assistente amigável que responde perguntas usando apenas o contexto fornecido.\n"
    "Pergunta: {pergunta}\n\n"
    "Contexto:\n{contexto}\n\n"
    "Responda de forma clara e concisa. "
    "Se a resposta não estiver no contexto, diga: 'Não encontrei essa informação no contexto'.\n"
    "Inclua a fonte no formato [fonte: título]."
)


# 3. Função para formatar documentos
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
        blocos.append(f"[fonte: {fonte}]\n{d.page_content}")
    return "\n\n---\n\n".join(blocos)


# 4. Função principal de QA
def answer_linear(pergunta: str):
    docs = retriever.invoke(pergunta)  # buscar documentos relevantes
    contexto = format_docs(docs)  # formatar contexto
    msg = qa_prompt.format_messages(pergunta=pergunta, contexto=contexto)
    out = llm.invoke(msg)  # gerar resposta com LLM
    return out.content


# 5. Entrada do usuário: pergunta
pergunta = input("\nDigite sua pergunta: ")
response = answer_linear(pergunta)
print(f"\nLLM: {response}")
