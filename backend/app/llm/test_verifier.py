from app.rag.retriever import retrieve_evidence
from app.llm.verifier import verify_claim


if __name__ == "__main__":

    claim = "Drinking lemon water cures diabetes."

    print("\nRetrieving evidence...")

    evidence = retrieve_evidence(
        claim,
        k=2,
    )

    print(f"Evidence retrieved: {len(evidence)}")

    print("\nSending claim and evidence to Llama...")

    result = verify_claim(
        claim,
        evidence,
    )

    print("\n--- VERIFICATION RESULT ---")

    print(f"Verdict: {result.get('verdict')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Explanation: {result.get('explanation')}")
    print(f"Evidence used: {result.get('evidence_used')}")