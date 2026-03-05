from pathlib import Path

from langchain_community.document_loaders import (
    BSHTMLLoader,
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = (
    Path(__file__).resolve().parent.parent.parent
)  # sobe de src/m3aula3 para raiz
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_m3a3"


# Função para criar/ler pasta data, carregar PDFs, txt, MK e html em documents
def load_docs(docs_dir: Path = DATA_DIR):
    docs_path = Path(docs_dir)
    docs_path.mkdir(parents=True, exist_ok=True)

    pdf_loader = DirectoryLoader(
        str(docs_dir),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,  # type: ignore
        show_progress=True,
    )
    txt_loader = DirectoryLoader(
        str(docs_dir),
        glob="**/*.txt",
        loader_cls=TextLoader,
        show_progress=True,
    )
    md_loader = DirectoryLoader(
        str(docs_dir),
        glob="**/*.md",
        loader_cls=TextLoader,
        show_progress=True,
    )
    html_loader = DirectoryLoader(
        str(docs_dir),
        glob="**/*.html",
        loader_cls=BSHTMLLoader,
        show_progress=True,
    )

    documents = []
    for loader in [pdf_loader, txt_loader, md_loader, html_loader]:
        try:
            documents.extend(loader.load())
        except Exception as e:
            print(f"[WARN] falha ao carregar com {loader}: {e}")
    if not documents:
        print(
            f"[INFO] Nenhum documento encontrado em '{docs_dir}', Crie/Coloque documentos em /data."
        )
    return documents


# Dividir documentos em chunks menores para uso nos embeddings e buscas semânticas
def split_docs(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=60,
        add_start_index=True,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)


# Criando banco com embeddings e persistencia
def build_chroma(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="meus_docs",
        persist_directory=str(CHROMA_DIR),
    )
    vectordb.persist()
    print(f"[OK] Chroma persistido na pasta chroma_m3a3")


if __name__ == "__main__":
    docs = load_docs(DATA_DIR)
    chunks = split_docs(docs)
    print(f"[OK] Documentos: {len(docs)} | Chunks: {len((chunks))}")
    build_chroma(chunks)
