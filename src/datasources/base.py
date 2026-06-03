from abc import ABC, abstractmethod
import pandas as pd


class DataSource(ABC):
    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def load_schema_summary(self) -> str:
        pass

    @abstractmethod
    def run_query(self, sql: str) -> pd.DataFrame:
        pass
