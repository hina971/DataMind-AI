from tools.ml_tools import run_ml_analysis


class MLAgent:

    name = "ML Agent"

    def run(self, state):

        state.add_log(
            "[ML Agent] Automatically identifying the prediction task..."
        )

        df = state.dataframe

        # --------------------------------------------------
        # Run automatic ML analysis
        # --------------------------------------------------

        results = run_ml_analysis(df)

        # --------------------------------------------------
        # Handle result
        # --------------------------------------------------

        if not results:

            state.ml_results = {
                "status": "FAILED",
                "message": "ML analysis could not be completed."
            }

            state.add_log(
                "[ML Agent] ML analysis could not be completed."
            )

            return state

        # Save results
        state.ml_results = results

        # --------------------------------------------------
        # Logging
        # --------------------------------------------------

        problem_type = results.get(
            "problem_type",
            "unknown"
        )

        target = results.get(
            "target",
            "not identified"
        )

        best_model = results.get(
            "best_model",
            "not available"
        )

        if problem_type == "classification":

            state.add_log(
                f"[ML Agent] Classification problem detected. "
                f"Target: {target}"
            )

        elif problem_type == "regression":

            state.add_log(
                f"[ML Agent] Regression problem detected. "
                f"Target: {target}"
            )

        else:

            state.add_log(
                f"[ML Agent] Problem type: {problem_type}. "
                f"Target: {target}"
            )

        state.add_log(
            f"[ML Agent] Models evaluated. "
            f"Best model: {best_model}"
        )

        return state
