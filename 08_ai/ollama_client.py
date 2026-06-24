import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ollama(
    prompt,
    model="qwen2.5:7b"
):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]