class ReviewerAgent:

    name = "Reviewer Agent"

    def run(self, state):

        state.add_log(
            "[Reviewer Agent] Reviewing data quality, "
            "statistical findings, ML results and visualizations..."
        )

        warnings = []

        q = state.quality_results or {}
        stats = state.statistical_results or {}
        ml = state.ml_results or {}
        viz = state.visualization_results or {}

        # =========================================================
        # 1. Missing Values
        # =========================================================

        missing_cells = q.get("missing_cells", 0)

        if missing_cells > 0:
            warnings.append(
                f"Missing values were detected ({missing_cells:,} cells). "
                "Appropriate imputation or missing-data handling should "
                "be considered before statistical analysis or modelling."
            )

        # =========================================================
        # 2. Duplicate Rows
        # =========================================================

        duplicate_rows = q.get("duplicate_rows", 0)

        if duplicate_rows > 0:
            warnings.append(
                f"{duplicate_rows:,} duplicate rows were detected. "
                "These records should be reviewed before modelling."
            )

        # =========================================================
        # 3. Outliers
        # =========================================================

        outliers = q.get("outliers", {})

        outlier_columns = [
            col
            for col, info in outliers.items()
            if isinstance(info, dict)
            and info.get("iqr_outliers", 0) > 0
        ]

        if outlier_columns:
            warnings.append(
                "Potential IQR-based outliers were detected in: "
                + ", ".join(outlier_columns)
                + ". These observations should be investigated "
                  "before removing or transforming them."
            )

        # =========================================================
        # 4. Constant Columns
        # =========================================================

        constants = q.get("constant_columns", [])

        if constants:
            warnings.append(
                "Constant variables detected: "
                + ", ".join(constants)
                + ". These variables provide little or no "
                  "predictive information."
            )

        # =========================================================
        # 5. Non-Normal Variables
        # =========================================================
        # IMPORTANT:
        # Non-normality is NOT treated as bad data.
        # It is a statistical characteristic of the distribution.

        non_normal = stats.get("non_normal_variables", [])

        if non_normal:

            state.add_log(
                "[Reviewer Agent] Non-normal distributions detected. "
                "This is not necessarily a data-quality problem."
            )

            warnings.append(
                "Some numerical variables show non-normal distributions. "
                "Non-normality does not mean the data is bad or incorrect; "
                "it indicates that the variable distribution should be "
                "considered when selecting statistical methods and "
                "interpreting results."
            )

        # =========================================================
        # 6. Information Overlap
        # =========================================================

        overlap_warnings = stats.get(
            "overlap_warnings",
            []
        )

        if overlap_warnings:

            for warning in overlap_warnings:
                warnings.append(warning)

            state.add_log(
                "[Reviewer Agent] Potential information overlap "
                "was identified among related variables."
            )

        # =========================================================
        # 7. Machine Learning Review
        # =========================================================

        if ml.get("status") == "OK":

            best_model = ml.get("best_model")

            if best_model:
                state.add_log(
                    f"[Reviewer Agent] Best ML model identified: "
                    f"{best_model}"
                )

            # Check whether stronger validation was used
            cv_method = ml.get("cv_method")

            if cv_method:
                state.add_log(
                    f"[Reviewer Agent] ML validation strategy: "
                    f"{cv_method}"
                )

            else:
                warnings.append(
                    "Baseline ML evaluation does not report "
                    "cross-validation or time-aware validation. "
                    "A stronger validation strategy is recommended "
                    "for reliable model comparison."
                )

        elif ml:

            warnings.append(
                "Machine-learning analysis was not completed successfully."
            )

        # =========================================================
        # 8. Visualization Review
        # =========================================================

        figures = viz.get("figures", [])

        if not figures:
            warnings.append(
                "No analytical visualizations were generated."
            )

        # =========================================================
        # 9. Reliability Assessment
        # =========================================================

        if len(warnings) == 0:

            reliability = "HIGH"

            reason = (
                "No major data-quality or methodological concerns "
                "were identified."
            )

        elif len(warnings) <= 2:

            reliability = "MODERATE"

            reason = (
                "The analysis is generally usable. Some statistical "
                "or methodological considerations should be reviewed "
                "before drawing strong conclusions."
            )

        else:

            reliability = "LOW"

            reason = (
                "Several important data-quality or methodological "
                "concerns were identified. Results should be "
                "interpreted cautiously."
            )

        # =========================================================
        # 10. Store Reviewer Results
        # =========================================================

        state.reviewer_results = {

            "reliability": reliability,

            "reason": reason,

            "warnings": warnings,

            "outlier_columns": outlier_columns,

            "constant_columns": constants,

            "non_normal_variables": non_normal,

            "overlap_warnings": overlap_warnings,

            "ml_validation_method": ml.get(
                "cv_method",
                None
            )

        }

        # =========================================================
        # 11. Final Reviewer Logs
        # =========================================================

        state.add_log(
            f"[Reviewer Agent] Reliability assessment: "
            f"{reliability}"
        )

        state.add_log(
            f"[Reviewer Agent] Review completed with "
            f"{len(warnings)} consideration(s)."
        )

        return state
