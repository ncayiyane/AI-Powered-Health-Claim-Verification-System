
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: list[Document],
) -> list[Document]:
    """
    Split documents into semantically meaningful chunks.

    Each chunk retains the original document metadata and is enriched
    with the document title and topic so that semantic retrieval has
    additional context.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    enriched_chunks = []

    for chunk in chunks:

        title = chunk.metadata.get(
            "title",
            "Unknown document"
        )

        topic = chunk.metadata.get(
            "topic",
            "Unknown topic"
        )

        context = (
            f"Title: {title}\n"
            f"Topic: {topic}\n\n"
        )

        chunk.page_content = (
            context + chunk.page_content
        )

        enriched_chunks.append(chunk)

    return enriched_chunks
