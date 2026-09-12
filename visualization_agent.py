
from tools.visualization_tools import generate_figures

class VisualizationAgent:
    name="Visualization Agent"
    def run(self,state):
        state.add_log("[Visualization Agent] Generating relevant visualizations...")
        state.visualization_results={"figures":generate_figures(state.dataframe,state.quality_results)}
        return state
