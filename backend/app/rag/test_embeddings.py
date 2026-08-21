from app.rag.document_loader import load_documents
from app.rag.chunker import chunk_documents
from app.rag.embeddings import get_embedding_model


documents = load_documents()
chunks = chunk_documents(documents)

embedding_model = get_embedding_model()

texts = [chunk.page_content for chunk in chunks]

embeddings = embedding_model.embed_documents(texts)

print(f"Chunks: {len(chunks)}")
print(f"Embeddings generated: {len(embeddings)}")

for index, embedding in enumerate(embeddings, start=1):
    print(f"\nChunk {index}")
    print(f"Vector dimensions: {len(embedding)}")
    print(f"First 10 values: {embedding[:10]}")