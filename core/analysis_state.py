
from dataclasses import dataclass, field
from typing import Any
import pandas as pd

@dataclass
class AnalysisState:
    user_request: str
    dataframe: pd.DataFrame
    dataset_info: dict = field(default_factory=dict)
    quality_results: dict = field(default_factory=dict)
    statistical_results: dict = field(default_factory=dict)
    ml_results: dict = field(default_factory=dict)
    visualization_results: dict = field(default_factory=dict)
    reviewer_results: dict = field(default_factory=dict)
    final_report: str = ""
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    activity_log: list = field(default_factory=list)
    log: Any = None

    def add_log(self, message):
        self.activity_log.append(message)
        if self.log:
            self.log(message)
