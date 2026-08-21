from app.rag.document_loader import load_documents
from app.rag.chunker import chunk_documents
from app.rag.vector_store import get_vector_store


def ingest_documents():
    print("Loading documents...")

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    chunks = chunk_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    vector_store = get_vector_store()

    # Clear the existing collection before re-ingesting.
    collection = vector_store._collection

    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])
        print(f"Removed {len(existing['ids'])} existing records.")

    vector_store.add_documents(chunks)

    print(f"Added {len(chunks)} chunks to ChromaDB.")
    print("Ingestion completed successfully.")


if __name__ == "__main__":
    ingest_documents()