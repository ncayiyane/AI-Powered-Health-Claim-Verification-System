from app.rag.retriever import retrieve_evidence
from app.llm.verifier import verify_claim


TEST_CLAIMS = [
    {
        "claim": "Regular physical activity provides health benefits.",
        "expected": "TRUE",
    },
    {
        "claim": "Vitamin C supplements can prevent or cure all illnesses.",
        "expected": "FALSE",
    },
    {
        "claim": "Exercise improves cardiovascular fitness and cures every disease.",
        "expected": "PARTIALLY_TRUE",
    },
    {
        "claim": "Drinking lemon water cures diabetes.",
        "expected": "UNVERIFIED",
    },
]


if __name__ == "__main__":

    print("\n========================================")
    print("HEALTH CLAIM VERIFICATION TEST SUITE")
    print("========================================")

    for index, test in enumerate(TEST_CLAIMS, start=1):

        claim = test["claim"]
        expected = test["expected"]

        print("\n----------------------------------------")
        print(f"TEST {index}")
        print("----------------------------------------")

        print(f"Claim: {claim}")
        print(f"Expected: {expected}")

        print("\nRetrieving evidence...")

        evidence = retrieve_evidence(
            claim,
            k=2,
        )

        print(f"Evidence retrieved: {len(evidence)}")

        if evidence:
            for evidence_index, item in enumerate(evidence, start=1):

                print(
                    f"Evidence {evidence_index}: "
                    f"{item['metadata'].get('title', 'Unknown')}"
                )

                print(
                    f"Distance: {item['distance']:.4f}"
                )

        print("\nSending claim and evidence to Llama...")

        result = verify_claim(
            claim,
            evidence,
        )

        verdict = result.get(
            "verdict",
            "UNVERIFIED"
        )

        confidence = result.get(
            "confidence",
            0.0
        )

        explanation = result.get(
            "explanation",
            ""
        )

        print("\n--- RESULT ---")

        print(f"Verdict: {verdict}")
        print(f"Confidence: {confidence}")
        print(f"Expected: {expected}")

        if verdict == expected:
            print("Status: PASS")
        else:
            print("Status: FAIL")

        print(f"Explanation: {explanation}")
        print(
            f"Evidence used: "
            f"{result.get('evidence_used', [])}"
        )