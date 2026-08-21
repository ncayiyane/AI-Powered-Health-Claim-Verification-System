from app.llm.client import generate_response


if __name__ == "__main__":

    prompt = """
    Explain diabetes in one short sentence.
    """

    response = generate_response(prompt)

    print("\n--- OLLAMA RESPONSE ---")
    print(response)