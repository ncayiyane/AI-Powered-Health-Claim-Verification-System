from app.rag.vector_store import get_vector_store


DEFAULT_DISTANCE_THRESHOLD = 0.8


def retrieve_evidence(
    query: str,
    k: int = 3,
    distance_threshold: float = DEFAULT_DISTANCE_THRESHOLD,
):
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    evidence = []

    for document, distance in results:

        distance = float(distance)

        # Lower Chroma distance means higher similarity.
        if distance > distance_threshold:
            continue

        evidence.append(
            {
                "content": document.page_content,
                "metadata": document.metadata,
                "distance": distance,
            }
        )

    return evidence