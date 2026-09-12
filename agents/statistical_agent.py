
from tools.statistical_tools import correlation_analysis, normality_summary

class StatisticalAgent:
    name="Statistical Agent"
    def run(self,state):
        state.add_log("[Statistical Agent] Checking statistical structure and assumptions...")
        state.statistical_results = {
            "correlations": correlation_analysis(state.dataframe),
            "normality": normality_summary(state.dataframe),
        }
        return state
