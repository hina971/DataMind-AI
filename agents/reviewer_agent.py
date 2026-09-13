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

        # ==================================================
        # 1. DATA QUALITY REVIEW
        # ==================================================

        missing_cells = q.get(
            "missing_cells",
            0
        )

        duplicate_rows = q.get(
            "duplicate_rows",
            0
        )

        if missing_cells > 0:

            warnings.append(
                f"Missing values were detected "
                f"({missing_cells:,} cells). "
                "Appropriate imputation or missing-data handling "
                "should be considered."
            )

        if duplicate_rows > 0:

            warnings.append(
                f"{duplicate_rows:,} duplicate rows were detected. "
                "These records should be reviewed before modelling."
            )

        # ==================================================
        # 2. OUTLIER REVIEW
        # ==================================================

        outliers = q.get(
            "outliers",
            {}
        )

        outlier_columns = [
            col
            for col, info in outliers.items()
            if isinstance(info, dict)
            and info.get(
                "iqr_outliers",
                0
            ) > 0
        ]

        if outlier_columns:

            warnings.append(
                "Potential IQR-based outliers were detected in: "
                + ", ".join(outlier_columns)
                + ". These observations should be investigated "
                  "before removing them."
            )

        # ==================================================
        # 3. CONSTANT VARIABLE REVIEW
        # ==================================================

        constants = q.get(
            "constant_columns",
            []
        )

        if constants:

            warnings.append(
                "Constant variables detected: "
                + ", ".join(constants)
                + ". These variables provide little or no "
                  "predictive information."
            )

        # ==================================================
        # 4. STATISTICAL REVIEW
        # ==================================================

        non_normal = stats.get(
            "non_normal_variables",
            []
        )

        if non_normal:

            warnings.append(
                "Potentially non-normal numerical variables "
                "were detected: "
                + ", ".join(non_normal)
                + ". Statistical assumptions should be "
                  "considered when interpreting results."
            )

        # ==================================================
        # 5. ML REVIEW
        # ==================================================

        if ml.get("status") == "OK":

            warnings.append(
                "Baseline ML evaluation uses a single holdout "
                "split; cross-validation is recommended for "
                "a stronger benchmark."
            )

            best_model = ml.get(
                "best_model"
            )

            if best_model:

                state.add_log(
                    f"[Reviewer Agent] Best ML model identified: "
                    f"{best_model}"
                )

        elif ml:

            warnings.append(
                "Machine-learning analysis was not completed "
                "successfully."
            )

        # ==================================================
        # 6. VISUALIZATION REVIEW
        # ==================================================

        figures = viz.get(
            "figures",
            []
        )

        if not figures:

            warnings.append(
                "No analytical visualizations were generated."
            )

        # ==================================================
        # 7. RELIABILITY ASSESSMENT
        # ==================================================

        if len(warnings) == 0:

            reliability = "HIGH"

            reason = (
                "No major data-quality, statistical, "
                "machine-learning or visualization issues "
                "were identified."
            )

        elif len(warnings) <= 2:

            reliability = "MODERATE"

            reason = (
                "The analysis is generally usable, but "
                "some methodological considerations should "
                "be reviewed before drawing strong conclusions."
            )

        else:

            reliability = "LOW"

            reason = (
                "Several data-quality or methodological "
                "issues were identified. Results should be "
                "interpreted cautiously."
            )

        # ==================================================
        # 8. SAVE REVIEW RESULTS
        # ==================================================

        state.reviewer_results = {

            "reliability":
                reliability,

            "reason":
                reason,

            "warnings":
                warnings,

            "outlier_columns":
                outlier_columns,

            "constant_columns":
                constants,

            "non_normal_variables":
                non_normal,
        }

        state.add_log(
            f"[Reviewer Agent] Reliability assessment: "
            f"{reliability}"
        )

        state.add_log(
            f"[Reviewer Agent] Review completed with "
            f"{len(warnings)} consideration(s)."
        )

        return state
