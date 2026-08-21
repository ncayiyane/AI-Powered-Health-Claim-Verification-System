from pathlib import Path

import chromadb
from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model


CHROMA_DIR = Path(__file__).resolve().parents[2] / "data" / "chroma"


def get_vector_store() -> Chroma:
    embedding_model = get_embedding_model()

    return Chroma(
        collection_name="health_evidence",
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_DIR),
    )