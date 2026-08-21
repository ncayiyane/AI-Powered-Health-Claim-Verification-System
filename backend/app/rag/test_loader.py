from app.rag.document_loader import load_documents
from app.rag.chunker import chunk_documents


documents = load_documents()

print(f"Documents loaded: {len(documents)}")

chunks = chunk_documents(documents)

print(f"Chunks created: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {index} ---")
    print(chunk.page_content)

    print("\nMetadata:")
    print(chunk.metadata)
    print("--- END CHUNK ---\n")
    