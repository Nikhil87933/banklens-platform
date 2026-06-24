from ollama_client import ask_ollama


def summarize_result(
    question,
    sql,
    rows
):

    prompt = f"""
You are a banking business analyst.

User Question:
{question}

Generated SQL:
{sql}

Query Result:
{rows}

Explain the result in simple business language.

Rules:
- Maximum 3 sentences.
- Be concise.
- Mention important numbers.
- Do not mention SQL.
- Do not invent information.
"""

    return ask_ollama(
        prompt,
        model="qwen2.5:7b"
    )