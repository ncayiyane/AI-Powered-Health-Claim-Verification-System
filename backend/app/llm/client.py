
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"

# Ollama can take longer when running an 8B model entirely on CPU.
# Keep the connection timeout short, but allow plenty of time for generation.
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 300


def generate_response(prompt: str) -> str:
    """
    Send a prompt to the local Ollama model and return
    the generated JSON response.

    The model runs locally through Ollama.
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0,
                },
            },
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
        )

        response.raise_for_status()

    except requests.exceptions.ConnectTimeout as exc:
        raise RuntimeError(
            "Could not connect to Ollama. "
            "Make sure Ollama is running on localhost:11434."
        ) from exc

    except requests.exceptions.ReadTimeout as exc:
        raise RuntimeError(
            "Ollama took too long to generate a response. "
            "The local LLM may be running slowly on the CPU."
        ) from exc

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Unable to connect to Ollama. "
            "Make sure the Ollama service is running."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(
            f"Ollama returned an HTTP error: {exc}"
        ) from exc

    data = response.json()

    generated_response = data.get("response")

    if not generated_response:
        raise RuntimeError(
            "Ollama returned an empty response."
        )

    return generated_response
