from openai import OpenAI

from src.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def generate_sql(user_question: str, schema_summary: str) -> str:
    prompt = f"""
You are a SQL assistant for an analytics database.

Rules:
- Use only the schema provided below.
- Generate only valid SQL.
- Only generate SELECT queries.
- You may use CTEs with WITH.
- Never use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, MERGE, CREATE, REPLACE, COPY, GRANT, or REVOKE.
- Prefer explicit JOINs.
- Add LIMIT 100 if the query returns row-level detail.
- Do not add LIMIT to aggregate/report queries unless needed.
- Return only SQL. No markdown fences. No explanation.

Schema:
{schema_summary}

User question:
{user_question}
"""

    response = client.responses.create(
        model=Config.OPENAI_MODEL,
        input=prompt,
    )

    return response.output_text.strip()
