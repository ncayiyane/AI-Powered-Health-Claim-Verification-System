from app.llm.client import LLM_PROVIDER, generate_response


if __name__ == "__main__":

    prompt = """
    Explain diabetes in one short sentence.
    """

    response = generate_response(prompt)

    print(f"\n--- {LLM_PROVIDER.upper()} RESPONSE ---")
    print(response)
