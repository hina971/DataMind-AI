from tools.visualization_tools import (
    generate_visualizations
)


class VisualizationAgent:

    name = "Visualization Agent"

    def run(self, state):

        state.add_log(
            "[Visualization Agent] Generating visual summaries..."
        )

        df = state.dataframe

        # ML results are already available
        # because the Orchestrator runs ML before Visualization.
        ml_results = state.ml_results

        # Generate all relevant visualizations
        results = generate_visualizations(
            df,
            ml_results
        )

        state.visualization_results = results

        total = results.get(
            "total_figures",
            0
        )

        state.add_log(
            f"[Visualization Agent] "
            f"Generated {total} visualization(s)."
        )

        return state
