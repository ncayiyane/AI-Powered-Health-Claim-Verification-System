import os

import requests
from dotenv import load_dotenv


# Load environment variables from backend/.env
load_dotenv()


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate",
)

MODEL_NAME = os.getenv(
    "OLLAMA_MODEL",
    "llama3.1:8b",
)


def get_timeout(name: str, default: int) -> int:
    """
    Read an integer timeout from an environment variable.

    Falls back to the default value if the environment variable
    is missing or contains an invalid value.
    """

    try:
        value = int(os.getenv(name, str(default)))

        if value <= 0:
            raise ValueError

        return value

    except (TypeError, ValueError):
        return default


CONNECT_TIMEOUT = get_timeout(
    "OLLAMA_CONNECT_TIMEOUT",
    10,
)

READ_TIMEOUT = get_timeout(
    "OLLAMA_READ_TIMEOUT",
    300,
)


def generate_response(prompt: str) -> str:
    """
    Send a prompt to the local Ollama model and return
    the generated JSON response.
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
            timeout=(
                CONNECT_TIMEOUT,
                READ_TIMEOUT,
            ),
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

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Ollama request failed: {exc}"
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "Ollama returned an invalid JSON response."
        ) from exc

    generated_response = data.get("response")

    if not generated_response:
        raise RuntimeError(
            "Ollama returned an empty response."
        )

    return generated_response