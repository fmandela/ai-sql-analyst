from src.config import Config
from src.datasources.duckdb_source import DuckDBSource
from src.datasources.snowflake_source import SnowflakeSource


def get_datasource():
    if Config.APP_DATASOURCE.lower() == "snowflake":
        return SnowflakeSource()
    return DuckDBSource()
