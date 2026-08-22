import json

from app.llm.client import generate_response
from app.llm.prompts import VERIFICATION_PROMPT


VALID_VERDICTS = {
    "TRUE",
    "FALSE",
    "PARTIALLY_TRUE",
    "UNVERIFIED",
}


def clean_json_response(response: str) -> str:
    """
    Remove Markdown code fences if the LLM returns them.
    """

    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

    return response


def verify_claim(claim: str, evidence: list) -> dict:

    evidence_text = ""

    for index, item in enumerate(evidence, start=1):

        metadata = item.get("metadata", {})

        title = metadata.get(
            "title",
            metadata.get("source_file", "Unknown")
        )

        source = metadata.get(
            "source",
            metadata.get(
                "source_organization",
                "Unknown source"
            )
        )

        relevance = item.get(
            "relevance_score",
            0.0
        )

        evidence_text += f"""
Evidence {index}

Title:
{title}

Source:
{source}

Relevance:
{relevance:.4f}

Content:
{item["content"]}

-------------------------
"""

    prompt = VERIFICATION_PROMPT.format(
        claim=claim,
        evidence=evidence_text,
    )

    response = generate_response(prompt)

    response = clean_json_response(response)

    try:
        result = json.loads(response)

    except json.JSONDecodeError:

        return {
            "verdict": "UNVERIFIED",
            "confidence": 0.0,
            "explanation": (
                "The AI returned an invalid verification response."
            ),
            "evidence_used": [],
            "raw_response": response,
        }

    # --------------------------------------------------
    # Validate verdict
    # --------------------------------------------------

    verdict = result.get(
        "verdict",
        "UNVERIFIED"
    )

    if verdict not in VALID_VERDICTS:
        verdict = "UNVERIFIED"

    # --------------------------------------------------
    # Validate confidence
    # --------------------------------------------------

    try:
        confidence = float(
            result.get(
                "confidence",
                0.0
            )
        )

    except (TypeError, ValueError):
        confidence = 0.0

    confidence = max(
        0.0,
        min(1.0, confidence)
    )

    # --------------------------------------------------
    # Validate explanation
    # --------------------------------------------------

    explanation = str(
        result.get(
            "explanation",
            "No explanation was provided."
        )
    )

    # --------------------------------------------------
    # Validate evidence_used
    # --------------------------------------------------

    raw_evidence_used = result.get(
        "evidence_used",
        []
    )

    if not isinstance(raw_evidence_used, list):
        raw_evidence_used = []

    valid_evidence_used = []

    for evidence_number in raw_evidence_used:

        try:
            evidence_number = int(
                evidence_number
            )

        except (TypeError, ValueError):
            continue

        # Evidence numbers are 1-based.
        if 1 <= evidence_number <= len(evidence):

            if evidence_number not in valid_evidence_used:
                valid_evidence_used.append(
                    evidence_number
                )

    # --------------------------------------------------
    # Safety fallback
    # --------------------------------------------------

    if verdict == "UNVERIFIED" and not valid_evidence_used:
        valid_evidence_used = []

    return {
        "verdict": verdict,
        "confidence": confidence,
        "explanation": explanation,
        "evidence_used": valid_evidence_used,
    }