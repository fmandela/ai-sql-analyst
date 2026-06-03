from openai import OpenAI

from src.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def explain_results(user_question: str, sql: str, result_preview: str) -> str:
    prompt = f"""
You are a practical data analyst assistant.

Given a user question, the SQL used, and a preview of the result, write a short plain-English explanation.
Do not invent facts beyond the result shown.
If the result is empty, say that clearly.
Mention any obvious caveats from the preview.

User question:
{user_question}

SQL:
{sql}

Result preview:
{result_preview}
"""

    response = client.responses.create(
        model=Config.OPENAI_MODEL,
        input=prompt,
    )

    return response.output_text.strip()
