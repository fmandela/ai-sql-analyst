from src.config import Config
from src.datasources.duckdb_source import DuckDBSource


def get_datasource():
    if Config.APP_DATASOURCE.lower() == "snowflake":
        pass  # Future SnowflakeSource implementation
    return DuckDBSource()
