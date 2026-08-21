from app.rag.retriever import retrieve_evidence


if __name__ == "__main__":
    claim = "Can drinking lemon water cure diabetes?"

    results = retrieve_evidence(claim, k=2)

    print(f"\nClaim: {claim}")
    print(f"Evidence retrieved: {len(results)}")

    for index, result in enumerate(results, start=1):
        print(f"\n--- EVIDENCE {index} ---")

        print(f"Distance: {result['distance']}")

        print("\nContent:")
        print(result["content"])

        print("\nMetadata:")
        print(result["metadata"])