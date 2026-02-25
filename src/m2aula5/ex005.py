from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import get_langchain_model

# Gerar embeddings locais
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Criar documentos locais a partir de texto
docs = [
    Document(
        page_content="A energia solar oferece benefícios ambientais e economicos.",
        metadata={"source": "Artigo 1", "date": "2025-01-10"},
    ),
    Document(
        page_content="O Flamengo é o maior time de futebol do mundo nas estatísticas da FIFA",
        metadata={"source": "Artigo 5", "date": "2024-11-15"},
    ),
    Document(
        page_content="A energia solar reduz a conta de luz por ser uma fonte renovável.",
        metadata={"source": "Artigo 2", "date": "2024-11-15"},
    ),
    Document(
        page_content="O campeonato brasileiro vai para por conta da data FIFA",
        metadata={"source": "Artigo 3", "date": "2023-12-01"},
    ),
    Document(
        page_content="O Flamengo é o maior time do mundo segundo o New York Times",
        metadata={"source": "Artigo 4", "date": "2026-02-20"},
    ),
]

# Salvar documentos no BD
vectorstore_meta = Chroma.from_documents(
    documents=docs, embedding=embeddings, collection_name="energia_solar_meta"
)

# Configurar retriever com k definido pelo usuário
retriever = vectorstore_meta.as_retriever(search_type="mmr", search_kwargs={"k": 4})

# Criação/Personalização do prompt
prompt_template = """
Você é um especialista em energia limpa, Excelente didática para crianças e um torcedor do flamengo.
Utilize SOMENTE os documentos fornecidos abaixo e esforce-se para responder à pergunta.
Se não houver informação suficiente nos documentos, responda que não sabe.

Documantos: {context}
Pergunta: {question}
Resposta:
"""

prompt = PromptTemplate.from_template(prompt_template)


# Função auxiliar para formatar os documentos em texto concatenado.
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Loop para variação de resposta de acordo com a temperatura.
for temp in [0.0, 0.5, 1.0]:
    llm = get_langchain_model(temperature=temp)

    # Pipeline que conecta retriever → formatação → prompt → LLM → parser.
    qa_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Chamada a llm
    # pergunta = "Como você explicaria energia solar para uma criança?"
    pergunta = "Como você explicaria o Flamengo para uma criança?"

    resposta = qa_chain.invoke(pergunta)

    print(f"\nTemperatura={temp}:\n{resposta}\n")
