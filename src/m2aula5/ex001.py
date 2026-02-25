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
def busca_top_k(query, k):
    results = vectorstore.similarity_search(query, k=k)
    print(f"\nResultados para top_k={k}: ")
    for i, r in enumerate(results):
        print(f"{i+1}. {r.page_content[:100]}...")


# Testar diferentes top_k
query = "Quem é o maior time do mundo?"
# query = "Quais são os benefícios da energia solar"
for k in [1, 4]:
    busca_top_k(query, k)
