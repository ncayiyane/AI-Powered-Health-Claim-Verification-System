import json

from app.llm.client import generate_response
from app.llm.prompts import VERIFICATION_PROMPT


def verify_claim(claim: str, evidence: list) -> dict:

    evidence_text = ""

    for index, item in enumerate(evidence, start=1):
        evidence_text += f"""
Evidence {index}:

{item["content"]}

Source:
{item["metadata"].get("source_file", "Unknown")}

Distance:
{item["distance"]}

-------------------------
"""

    prompt = VERIFICATION_PROMPT.format(
        claim=claim,
        evidence=evidence_text,
    )

    response = generate_response(prompt)

    # Remove possible markdown code fences
    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

    try:
        result = json.loads(response)

    except json.JSONDecodeError:

        return {
            "verdict": "UNVERIFIED",
            "confidence": 0.0,
            "explanation": "The AI returned an invalid verification response.",
            "evidence_used": [],
            "raw_response": response,
        }

    return result