
import re
from tools.ml_tools import choose_target, regression_models

class MLAgent:
    name="ML Agent"
    def run(self,state):
        state.add_log("[ML Agent] Preparing machine-learning analysis...")
        text=state.user_request.lower()
        requested=None
        for col in state.dataframe.columns:
            if col.lower() in text:
                requested=col; break
        target=choose_target(state.dataframe,requested)
        if target is None:
            state.ml_results={"status":"NOT_APPLICABLE","message":"No numeric target detected."}
        else:
            state.ml_results=regression_models(state.dataframe,target)
            state.add_log(f"[ML Agent] Regression target selected: {target}")
        return state
