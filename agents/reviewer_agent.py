
class ReviewerAgent:
    name="Reviewer Agent"
    def run(self,state):
        state.add_log("[Reviewer] Validating assumptions, results and limitations...")
        warnings=[]
        q=state.quality_results
        if q.get("missing_cells",0)>0:
            warnings.append("Missing values are present; treatment should be considered before inferential conclusions.")
        if q.get("duplicate_rows",0)>0:
            warnings.append("Duplicate records were detected.")
        if state.ml_results.get("status")=="OK":
            warnings.append("Baseline ML evaluation uses a single holdout split; cross-validation is recommended for a stronger benchmark.")
        if state.errors:
            warnings.extend(state.errors)
        if not warnings:
            reliability="HIGH"
            reason="No major automated data-quality warning was detected."
        elif len(warnings)<=2:
            reliability="MODERATE"
            reason="The analysis is usable, but the listed warnings should be considered."
        else:
            reliability="LOW"
            reason="Multiple issues may materially affect interpretation."
        state.reviewer_results={"reliability":reliability,"reason":reason,"warnings":warnings}
        state.add_log(f"[Reviewer] Reliability: {reliability}")
        return state
