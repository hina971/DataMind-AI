
from tools.data_quality_tools import profile_dataset, detect_outliers

class DataQualityAgent:
    name="Data Quality Agent"
    def run(self,state):
        state.add_log("[Data Quality Agent] Profiling dataset...")
        q=profile_dataset(state.dataframe)
        q["outliers"]=detect_outliers(state.dataframe)
        state.quality_results=q
        state.dataset_info=q
        state.add_log(f"[Data Quality Agent] Found {q['missing_cells']} missing cells and {q['duplicate_rows']} duplicate rows.")
        return state
