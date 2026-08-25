
from pathlib import Path

from langchain_core.documents import Document


DOCUMENTS_DIR = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "documents"
)


def extract_metadata(text: str) -> dict:
    """
    Extract metadata from document text.

    Supported fields:
    - Title
    - Source
    - Source URL
    - Topic
    - Source organization
    """

    metadata = {}

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Check Source URL before Source because
        # "Source URL:" also begins with "Source:".
        if line.startswith("Source URL:"):
            metadata["url"] = line.replace(
                "Source URL:",
                "",
                1
            ).strip()

        elif line.startswith("Title:"):
            metadata["title"] = line.replace(
                "Title:",
                "",
                1
            ).strip()

        elif line.startswith("Source:"):
            metadata["source"] = line.replace(
                "Source:",
                "",
                1
            ).strip()

        elif line.startswith("Topic:"):
            metadata["topic"] = line.replace(
                "Topic:",
                "",
                1
            ).strip()

        elif line.startswith("Source organization:"):
            metadata["source_organization"] = line.replace(
                "Source organization:",
                "",
                1
            ).strip()

    return metadata


def load_documents() -> list[Document]:
    """
    Load all .txt documents from the documents directory.

    Each document is converted into a LangChain Document
    containing its text and extracted metadata.
    """

    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        metadata = {
            "source_file": file_path.name,
            "source_path": str(file_path),
        }

        # Extract metadata defined inside the document.
        extracted_metadata = extract_metadata(text)

        metadata.update(extracted_metadata)

        documents.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    return documents
