from app.rag.vector_store import get_vector_store


def calculate_relevance(distance: float) -> float:
    """
    Convert ChromaDB distance into a bounded relevance score.

    This is a relative relevance indicator, NOT a probability
    and NOT the final verification confidence.
    """

    return 1.0 / (1.0 + distance)


def retrieve_evidence(
    query: str,
    k: int = 3,
):
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    evidence = []

    for document, distance in results:

        distance = float(distance)

        evidence.append(
            {
                "content": document.page_content,
                "metadata": document.metadata,
                "distance": distance,
                "relevance_score": calculate_relevance(distance),
            }
        )

    return evidence