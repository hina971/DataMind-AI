
from agents.data_quality_agent import DataQualityAgent
from agents.statistical_agent import StatisticalAgent
from agents.ml_agent import MLAgent
from agents.visualization_agent import VisualizationAgent
from agents.reviewer_agent import ReviewerAgent
from reports.report_generator import generate_report

class OrchestratorAgent:
    name="Orchestrator Agent"

    def run(self,state):
        state.add_log("[Orchestrator] Understanding user request...")
        text=state.user_request.lower()

        DataQualityAgent().run(state)

        complete = any(x in text for x in ["complete","full","overall","analyze"])
        wants_quality = any(x in text for x in ["missing","outlier","duplicate","quality","profile"])
        wants_stats = any(x in text for x in ["correlation","statistical","statistics","test","relationship","overview"])
        wants_ml = any(x in text for x in ["predict","machine learning","model","regression","classification","forecast"])
        wants_viz = any(x in text for x in ["plot","chart","visual","visualization","graph"])
        if complete:
            wants_stats=wants_ml=wants_viz=True

        if wants_stats:
            StatisticalAgent().run(state)
        if wants_ml:
            MLAgent().run(state)
        if wants_viz or complete:
            VisualizationAgent().run(state)

        ReviewerAgent().run(state)
        state.final_report=generate_report(state)
        return state
