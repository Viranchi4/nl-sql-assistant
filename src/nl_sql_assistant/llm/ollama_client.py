import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5-coder:3b"


def generate_text(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Send a prompt to a locally running Ollama model
    and return the generated text.
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "seed": 42,
        },
    }

    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

    except (HTTPError, URLError) as error:
        raise RuntimeError(
            "Unable to communicate with Ollama. "
            "Make sure Ollama is running."
        ) from error

    return result["response"].strip()