from app.rag.vector_store import get_vector_store


def search_evidence(query: str, k: int = 2):
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    return results


if __name__ == "__main__":
    query = "Diabetes is a chronic disease."

    results = search_evidence(query)

    print(f"\nQuery: {query}")
    print(f"Results found: {len(results)}")

    for index, (document, score) in enumerate(results, start=1):
        print(f"\n--- RESULT {index} ---")
        print(f"Similarity score: {score}")

        print("\nContent:")
        print(document.page_content)

        print("\nMetadata:")
        print(document.metadata)