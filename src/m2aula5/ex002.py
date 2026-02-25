from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

# Gerar embeddings locais
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Criar documentos locais a partir de texto
docs = [
    Document(
        page_content="A energia solar oferece benefícios ambientais e economicos.",
        metadata={"source": "Artigo 1"},
    ),
    Document(
        page_content="A energia solar reduz a conta de luz por ser uma fonte renovável.",
        metadata={"source": "Artigo 2"},
    ),
    Document(
        page_content="O campeonato brasileiro vai para por conta da data FIFA",
        metadata={"source": "Artigo 3"},
    ),
    Document(
        page_content="O Flamengo é o maior time do mundo segundo o New York Times",
        metadata={"source": "Artigo 4"},
    ),
]

# Salvar documentos no BD
vectorstore = Chroma.from_documents(
    documents=docs, embedding=embeddings, collection_name="energia_solar"
)


# Função para busca variando o top_k
def busca_com_filtro_score(query, threshould=0.7, k=3):
    results = vectorstore._similarity_search_with_relevance_scores(query, k=k)
    filtrados = [(doc, score) for doc, score in results if score >= threshould]
    print(f"\nDocumentos com score >= {threshould} (top_k={k}): ")
    for doc, score in filtrados:
        print(f"Score: {score:.2f} | Conteúdo: {doc.page_content[:120]}...")


# Testar Filtros
query = "Quais são os benefícios da energia solar"
# query = "Quem é o maior time do mundo?"
for threshould in [0.4, 0.6, 0.7]:
    busca_com_filtro_score(query, threshould)
