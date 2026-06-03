import re

BLOCKED_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "MERGE",
    "CREATE", "REPLACE", "GRANT", "REVOKE", "CALL", "COPY", "PUT", "REMOVE"
]


def validate_sql(sql: str) -> tuple[bool, str]:
    if not sql or not sql.strip():
        return False, "SQL is empty."

    cleaned = sql.strip().rstrip(";")
    normalized = cleaned.upper()

    if ";" in cleaned:
        return False, "Multiple statements are not allowed."

    if not (normalized.startswith("SELECT") or normalized.startswith("WITH")):
        return False, "Only SELECT queries are allowed."

    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf"\b{keyword}\b", normalized):
            return False, f"Blocked keyword detected: {keyword}"

    return True, "SQL is valid."
