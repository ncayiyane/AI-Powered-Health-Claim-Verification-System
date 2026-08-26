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
    Clean common formatting issues from an LLM response.
    """

    response = response.strip()

    # Remove Markdown code fences if present.
    if response.startswith("```"):
        lines = response.splitlines()

        cleaned_lines = []

        for line in lines:
            if line.strip().startswith("```"):
                continue

            cleaned_lines.append(line)

        response = "\n".join(cleaned_lines).strip()

    # Occasionally the model may return text before or after JSON.
    # Try to isolate the JSON object.
    first_brace = response.find("{")
    last_brace = response.rfind("}")

    if first_brace != -1 and last_brace != -1:
        response = response[first_brace:last_brace + 1]

    return response


def verify_claim(claim: str, evidence: list) -> dict:

    # --------------------------------------------------
    # 1. Build evidence context
    # --------------------------------------------------

    evidence_text = ""

    for index, item in enumerate(evidence, start=1):

        metadata = item.get(
            "metadata",
            {}
        )

        title = metadata.get(
            "title",
            metadata.get(
                "source_file",
                "Unknown"
            )
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
{item.get("content", "")}

-------------------------
"""

    # --------------------------------------------------
    # 2. Build verification prompt
    # --------------------------------------------------

    prompt = VERIFICATION_PROMPT.format(
        claim=claim,
        evidence=evidence_text,
    )

    # --------------------------------------------------
    # 3. Ask Llama for structured JSON
    # --------------------------------------------------

    response = generate_response(prompt)

    response = clean_json_response(response)

    # --------------------------------------------------
    # 4. Parse JSON
    # --------------------------------------------------

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
    # 5. Make sure the response is an object
    # --------------------------------------------------

    if not isinstance(result, dict):

        return {
            "verdict": "UNVERIFIED",
            "confidence": 0.0,
            "explanation": (
                "The AI returned an invalid verification structure."
            ),
            "evidence_used": [],
            "raw_response": response,
        }

    # --------------------------------------------------
    # 6. Validate verdict
    # --------------------------------------------------

    verdict = result.get(
        "verdict",
        "UNVERIFIED"
    )

    if not isinstance(verdict, str):
        verdict = "UNVERIFIED"

    verdict = verdict.strip().upper()

    if verdict not in VALID_VERDICTS:
        verdict = "UNVERIFIED"

    # --------------------------------------------------
    # 7. Validate confidence
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
        min(
            1.0,
            confidence
        )
    )

    # --------------------------------------------------
    # 8. Validate explanation
    # --------------------------------------------------

    explanation = result.get(
        "explanation",
        "No explanation was provided."
    )

    if not isinstance(explanation, str):
        explanation = str(explanation)

    explanation = explanation.strip()

    if not explanation:
        explanation = "No explanation was provided."

    # --------------------------------------------------
    # 9. Validate evidence_used
    # --------------------------------------------------

    raw_evidence_used = result.get(
        "evidence_used",
        []
    )

    if not isinstance(
        raw_evidence_used,
        list
    ):
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
        if (
            1 <= evidence_number <= len(evidence)
            and evidence_number not in valid_evidence_used
        ):

            valid_evidence_used.append(
                evidence_number
            )

    # --------------------------------------------------
    # 10. Return normalized result
    # --------------------------------------------------

    return {
        "verdict": verdict,
        "confidence": confidence,
        "explanation": explanation,
        "evidence_used": valid_evidence_used,
    }