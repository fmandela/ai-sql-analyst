from pathlib import Path
import duckdb
import pandas as pd

from src.datasources.base import DataSource


class DuckDBSource(DataSource):
    def __init__(self, db_path: str = "demo.duckdb"):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)

    def initialize(self) -> None:
        data_dir = Path("data/microfinance")
        csv_files = {
            "offices": data_dir / "offices.csv",
            "customers": data_dir / "customers.csv",
            "products": data_dir / "products.csv",
            "loans": data_dir / "loans.csv",
            "repayments": data_dir / "repayments.csv",
        }

        for table_name, csv_path in csv_files.items():
            if not csv_path.exists():
                raise FileNotFoundError(f"Missing demo data file: {csv_path}")
            self.conn.execute(
                f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_path.as_posix()}')"
            )

    def load_schema_summary(self) -> str:
        tables = self.conn.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'main'
            ORDER BY table_name
        """).fetchdf()

        if tables.empty:
            return "No tables found. Load the demo environment first."

        lines = []
        for table_name in tables["table_name"].tolist():
            columns = self.conn.execute(f"DESCRIBE {table_name}").fetchdf()
            row_count = self.conn.execute(f"SELECT COUNT(*) AS row_count FROM {table_name}").fetchone()[0]
            lines.append(f"\nTable: {table_name} ({row_count} rows)")
            for _, row in columns.iterrows():
                lines.append(f"- {row['column_name']} ({row['column_type']})")

        return "\n".join(lines).strip()

    def run_query(self, sql: str) -> pd.DataFrame:
        return self.conn.execute(sql).fetchdf()
