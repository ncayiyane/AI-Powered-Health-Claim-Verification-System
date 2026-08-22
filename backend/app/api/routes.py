from fastapi import APIRouter

from app.models.schemas import ClaimRequest, VerificationResponse, Verdict
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

    # --------------------------------------------------
    # 1. Retrieve relevant evidence from ChromaDB
    # --------------------------------------------------

    evidence = retrieve_evidence(
        request.claim,
        k=2
    )

    # --------------------------------------------------
    # 2. Send claim + evidence to Llama
    # --------------------------------------------------

    verification = verify_claim(
        request.claim,
        evidence
    )

    # --------------------------------------------------
    # 3. Determine which evidence Llama actually used
    # --------------------------------------------------

    evidence_used = verification.get(
        "evidence_used",
        []
    )

    selected_evidence = []

    for evidence_number in evidence_used:

        try:
            index = int(evidence_number) - 1
        except (TypeError, ValueError):
            continue

        if 0 <= index < len(evidence):
            selected_evidence.append(
                evidence[index]
            )

    # If the LLM did not provide valid evidence numbers,
    # fall back to the retrieved evidence.
    if not selected_evidence:
        selected_evidence = evidence

    # --------------------------------------------------
    # 4. Convert evidence into API response format
    # --------------------------------------------------

    evidence_items = []

    for item in selected_evidence:

        metadata = item.get(
            "metadata",
            {}
        )

        distance = float(
            item.get(
                "distance",
                0.0
            )
        )

        # Convert Chroma distance into a normalized
        # relevance score between 0 and 1.
        relevance_score = max(
            0.0,
            min(
                1.0,
                1.0 / (1.0 + distance)
            )
        )

        evidence_items.append(
            {
                "title": metadata.get(
                    "title",
                    metadata.get(
                        "source_file",
                        "Unknown"
                    )
                ),

                "source": metadata.get(
                    "source",
                    metadata.get(
                        "source_organization",
                        "Unknown source"
                    )
                ),

                "url": metadata.get(
                    "url"
                ),

                "snippet": item.get(
                    "content",
                    ""
                ),

                "relevance_score": relevance_score
            }
        )

    # --------------------------------------------------
    # 5. Validate verdict
    # --------------------------------------------------

    verdict_value = verification.get(
        "verdict",
        "UNVERIFIED"
    )

    try:
        verdict = Verdict(verdict_value)
    except ValueError:
        verdict = Verdict.UNVERIFIED

    # --------------------------------------------------
    # 6. Return final verification result
    # --------------------------------------------------

    return VerificationResponse(
        claim=request.claim,

        verdict=verdict,

        confidence=float(
            verification.get(
                "confidence",
                0.0
            )
        ),

        explanation=verification.get(
            "explanation",
            "Unable to generate an explanation."
        ),

        evidence=evidence_items
    )