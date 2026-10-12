import os

import requests
from dotenv import load_dotenv


# Load environment variables from backend/.env
load_dotenv()


LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama",
).strip().lower()


# ============================================================
# Ollama configuration
# ============================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.1:8b",
)


# ============================================================
# Groq configuration
# ============================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    "",
).strip()

GROQ_URL = os.getenv(
    "GROQ_URL",
    "https://api.groq.com/openai/v1/chat/completions",
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant",
)


# ============================================================
# Timeout configuration
# ============================================================

def get_timeout(name: str, default: int) -> int:
    """
    Read an integer timeout from an environment variable.

    Falls back to the default value if the environment variable
    is missing or contains an invalid value.
    """

    try:
        value = int(
            os.getenv(
                name,
                str(default),
            )
        )

        if value <= 0:
            raise ValueError

        return value

    except (TypeError, ValueError):
        return default


OLLAMA_CONNECT_TIMEOUT = get_timeout(
    "OLLAMA_CONNECT_TIMEOUT",
    10,
)

OLLAMA_READ_TIMEOUT = get_timeout(
    "OLLAMA_READ_TIMEOUT",
    300,
)

GROQ_CONNECT_TIMEOUT = get_timeout(
    "GROQ_CONNECT_TIMEOUT",
    10,
)

GROQ_READ_TIMEOUT = get_timeout(
    "GROQ_READ_TIMEOUT",
    120,
)


# ============================================================
# Ollama provider
# ============================================================

def _generate_with_ollama(prompt: str) -> str:
    """
    Generate a response using the local Ollama server.
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0,
                },
            },
            timeout=(
                OLLAMA_CONNECT_TIMEOUT,
                OLLAMA_READ_TIMEOUT,
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


# ============================================================
# Groq provider
# ============================================================

def _generate_with_groq(prompt: str) -> str:
    """
    Generate a response using the Groq Chat Completions API.
    """

    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0,
        "stream": False,
        "response_format": {
            "type": "json_object",
        },
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=(
                GROQ_CONNECT_TIMEOUT,
                GROQ_READ_TIMEOUT,
            ),
        )

        response.raise_for_status()

    except requests.exceptions.ConnectTimeout as exc:
        raise RuntimeError(
            "Could not connect to Groq."
        ) from exc

    except requests.exceptions.ReadTimeout as exc:
        raise RuntimeError(
            "Groq took too long to generate a response."
        ) from exc

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Unable to connect to Groq. "
            "Check your internet connection."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        try:
            error_details = response.json()
        except ValueError:
            error_details = response.text

        raise RuntimeError(
            f"Groq returned an HTTP error: "
            f"{exc}. Details: {error_details}"
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Groq request failed: {exc}"
        ) from exc

    try:
        data = response.json()

    except ValueError as exc:
        raise RuntimeError(
            "Groq returned an invalid JSON response."
        ) from exc

    try:
        generated_response = (
            data["choices"][0]["message"]["content"]
        )

    except (
        KeyError,
        IndexError,
        TypeError,
    ) as exc:
        raise RuntimeError(
            "Groq returned an unexpected response structure."
        ) from exc

    if not generated_response:
        raise RuntimeError(
            "Groq returned an empty response."
        )

    return generated_response


# ============================================================
# Provider dispatcher
# ============================================================

def generate_response(prompt: str) -> str:
    """
    Generate an LLM response using the configured provider.

    Supported providers:
        - ollama
        - groq
    """

    if LLM_PROVIDER == "ollama":
        return _generate_with_ollama(prompt)

    if LLM_PROVIDER == "groq":
        return _generate_with_groq(prompt)

    raise RuntimeError(
        f"Unsupported LLM provider: {LLM_PROVIDER}. "
        "Supported providers are: ollama, groq."
    )