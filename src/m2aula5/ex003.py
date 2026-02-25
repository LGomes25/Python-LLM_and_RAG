from datetime import datetime

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

# Gerar embeddings locais
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Criar documentos locais a partir de texto
docs = [
    Document(
        page_content="A energia solar oferece benefícios ambientais e economicos.",
        metadata={"source": "Artigo 1", "date": "2025-01-10"},
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


# Função para busca variando o top_k
def busca_por_data(query, data_limite):
    results = vectorstore_meta.similarity_search(query, k=10)
    filtrados = []
    for doc in results:
        # Recupera a string da metadata
        date_str = doc.metadata.get("date", "1900-01-01")
        # Converte para datetime
        doc_date = datetime.strptime(date_str, "%Y-%m-%d")
        # Faz a comparação
        if doc_date > data_limite:
            filtrados.append(doc)

    print(f"\nDocumentos após {data_limite.strftime('%Y-%m-%d')}: ")
    for doc in filtrados:
        print(f"- {doc.page_content} (Data: {doc.metadata['date']})")


# Testar Filtros
query = "Quais são os benefícios da energia solar"
busca_por_data(query, datetime(2024, 10, 1))
