
import re

from app.rag.vector_store import get_vector_store


# Chroma uses distance where LOWER means MORE similar.
DEFAULT_DISTANCE_THRESHOLD = 1.5


# Common words that do not help determine whether evidence
# is relevant to the actual health claim.
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "be",
    "can",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "what",
    "when",
    "with",
    "will",
}


def _tokenize(text: str) -> set[str]:
    """
    Convert text into a set of meaningful lowercase words.
    """

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

    return {
        word
        for word in words
        if word not in STOP_WORDS
    }


def _calculate_keyword_overlap(
    query: str,
    content: str,
) -> int:
    """
    Calculate how many meaningful query words also appear
    in the evidence content.
    """

    query_words = _tokenize(query)
    content_words = _tokenize(content)

    return len(query_words.intersection(content_words))


def _topic_matches(
    query: str,
    metadata: dict,
) -> bool:
    """
    Check whether the document topic is directly related
    to the claim.

    Example:
        Query: "Can drinking lemon water cure diabetes?"
        Topic: "Diabetes"

    This should return True.
    """

    topic = metadata.get("topic", "")

    if not topic:
        return False

    query_words = _tokenize(query)
    topic_words = _tokenize(topic)

    return bool(query_words.intersection(topic_words))


def retrieve_evidence(
    query: str,
    k: int = 3,
    distance_threshold: float = DEFAULT_DISTANCE_THRESHOLD,
):
    """
    Retrieve relevant evidence from ChromaDB.

    Evidence is accepted when at least one of the following
    conditions is satisfied:

    1. Semantic similarity is strong enough.
    2. The document topic directly matches the claim.
    3. The evidence contains multiple meaningful keywords
       from the claim.

    This prevents unrelated semantically similar documents
    from automatically being accepted as evidence.
    """

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    evidence = []

    for document, distance in results:

        distance = float(distance)

        content = document.page_content
        metadata = document.metadata or {}

        keyword_overlap = _calculate_keyword_overlap(
            query,
            content,
        )

        topic_match = _topic_matches(
            query,
            metadata,
        )

        strong_semantic_match = (
            distance <= distance_threshold
        )

        strong_keyword_match = (
            keyword_overlap >= 2
        )

        # Reject documents that are only vaguely similar.
        if not (
            strong_semantic_match
            and (
                topic_match
                or strong_keyword_match
            )
        ):
            continue

        evidence.append(
            {
                "content": content,
                "metadata": metadata,
                "distance": distance,
                "keyword_overlap": keyword_overlap,
                "topic_match": topic_match,
            }
        )

    # Best evidence first:
    # 1. Topic relevance
    # 2. Keyword overlap
    # 3. Semantic distance
    evidence.sort(
        key=lambda item: (
            not item["topic_match"],
            -item["keyword_overlap"],
            item["distance"],
        )
    )

    return evidence
