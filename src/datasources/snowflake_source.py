import pandas as pd
import snowflake.connector

from src.config import Config
from src.datasources.base import DataSource


class SnowflakeSource(DataSource):
    def __init__(self):
        self.connection_args = {
            "account": Config.SNOWFLAKE_ACCOUNT,
            "user": Config.SNOWFLAKE_USER,
            "password": Config.SNOWFLAKE_PASSWORD,
            "warehouse": Config.SNOWFLAKE_WAREHOUSE,
            "database": Config.SNOWFLAKE_DATABASE,
            "schema": Config.SNOWFLAKE_SCHEMA,
            "role": Config.SNOWFLAKE_ROLE,
        }

    def _connect(self):
        return snowflake.connector.connect(**self.connection_args)

    def initialize(self) -> None:
        # Snowflake setup is intentionally external for now.
        # Run sql/create_tables.sql and sql/seed_data.sql manually when using Snowflake.
        return None

    def run_query(self, sql: str) -> pd.DataFrame:
        conn = self._connect()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            return cur.fetch_pandas_all()
        finally:
            cur.close()
            conn.close()

    def load_schema_summary(self) -> str:
        sql = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = CURRENT_SCHEMA()
        ORDER BY table_name, ordinal_position
        """
        df = self.run_query(sql)

        if df.empty:
            return "No tables found in the current Snowflake schema."

        lines = []
        current_table = None
        for _, row in df.iterrows():
            table_name = row["TABLE_NAME"]
            if table_name != current_table:
                lines.append(f"\nTable: {table_name}")
                current_table = table_name
            lines.append(f"- {row['COLUMN_NAME']} ({row['DATA_TYPE']})")

        return "\n".join(lines).strip()
