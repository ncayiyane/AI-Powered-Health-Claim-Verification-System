from fastapi import APIRouter

from app.models.schemas import ClaimRequest, VerificationResponse, EvidenceItem
from app.rag.retriever import retrieve_evidence
from app.llm.verifier import verify_claim


router = APIRouter(
    prefix="/api/v1/claims",
    tags=["Health Claim Verification"]
)


@router.post(
    "/verify",
    response_model=VerificationResponse
)
def verify_health_claim(request: ClaimRequest):

    # ---------------------------------------------------------
    # 1. Retrieve relevant evidence from ChromaDB
    # ---------------------------------------------------------

    retrieved_evidence = retrieve_evidence(
        request.claim,
        k=2
    )

    # ---------------------------------------------------------
    # 2. Send claim + evidence to the LLM
    # ---------------------------------------------------------

    verification = verify_claim(
        request.claim,
        retrieved_evidence
    )

    # ---------------------------------------------------------
    # 3. Convert retrieved evidence into API response format
    # ---------------------------------------------------------

    evidence_items = []

    for item in retrieved_evidence:

        metadata = item.get("metadata", {})

        evidence_items.append(
    EvidenceItem(
        title=metadata.get(
            "title",
            metadata.get("source_file", "Unknown source")
        ),
        source=metadata.get(
            "source",
            metadata.get(
                "source_organization",
                "Unknown source"
            )
        ),
        url=None,
        snippet=item.get("content", ""),
        relevance_score=float(
            item.get("relevance_score", 0.0)
        )
    )
)

    # ---------------------------------------------------------
    # 4. Return final verification result
    # ---------------------------------------------------------

    return VerificationResponse(
        claim=request.claim,
        verdict=verification.get(
            "verdict",
            "UNVERIFIED"
        ),
        confidence=float(
            verification.get(
                "confidence",
                0.0
            )
        ),
        explanation=verification.get(
            "explanation",
            "Unable to generate a verification explanation."
        ),
        evidence=evidence_items
    )