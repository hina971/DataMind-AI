from tools.statistical_tools import (
    correlation_analysis,
    normality_summary
)


class StatisticalAgent:

    name = "Statistical Agent"

    def run(self, state):

        state.add_log(
            "[Statistical Agent] Checking statistical structure and assumptions..."
        )

        df = state.dataframe

        # ---------------------------------------------------------
        # 1. Correlation Analysis
        # ---------------------------------------------------------

        correlations = correlation_analysis(df)

        # ---------------------------------------------------------
        # 2. Normality Analysis
        # ---------------------------------------------------------

        normality = normality_summary(df)

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        findings = []

        findings.append(
            f"The dataset contains {len(numeric_columns)} "
            "numerical variables suitable for statistical analysis."
        )

        # ---------------------------------------------------------
        # 3. Extract strongest correlations
        # ---------------------------------------------------------

        pearson = correlations.get("pearson", {})
        relationships = []

        if isinstance(pearson, dict):

            for variable, values in pearson.items():

                if not isinstance(values, dict):
                    continue

                for other, value in values.items():

                    if variable == other:
                        continue

                    try:
                        value = float(value)

                        pair = tuple(
                            sorted([variable, other])
                        )

                        relationships.append(
                            (
                                pair[0],
                                pair[1],
                                value
                            )
                        )

                    except (TypeError, ValueError):
                        continue

        # Remove duplicate pairs

        unique_relationships = {}

        for variable_a, variable_b, value in relationships:

            key = (
                variable_a,
                variable_b
            )

            if key not in unique_relationships:

                unique_relationships[key] = value

        strongest = sorted(
            [
                (a, b, value)
                for (a, b), value
                in unique_relationships.items()
            ],
            key=lambda x: abs(x[2]),
            reverse=True
        )[:5]

        # ---------------------------------------------------------
        # 4. Human-readable correlation findings
        # ---------------------------------------------------------

        if strongest:

            findings.append(
                "The correlation analysis identified the strongest "
                "relationships between numerical variables."
            )

            for variable_a, variable_b, value in strongest:

                if abs(value) >= 0.70:

                    strength = "strong"

                elif abs(value) >= 0.40:

                    strength = "moderate"

                else:

                    strength = "weak"

                if value > 0:

                    direction = "positive"

                elif value < 0:

                    direction = "negative"

                else:

                    direction = "negligible"

                findings.append(
                    f"{variable_a} and {variable_b} show a "
                    f"{strength} {direction} relationship "
                    f"(Pearson r = {value:.3f})."
                )

        else:

            findings.append(
                "No meaningful correlation relationships "
                "could be identified."
            )

        # ---------------------------------------------------------
        # 5. NEW IMPROVEMENT:
        #    Temperature / DewPoint information overlap
        # ---------------------------------------------------------

        overlap_warnings = []

        columns_lower = {
            str(col).lower(): col
            for col in df.columns
        }

        temperature_col = None
        dewpoint_col = None

        for name, original in columns_lower.items():

            # Find Temperature column
            if (
                "temperature" in name
                and "dew" not in name
            ):
                temperature_col = original

            # Find DewPoint column
            if (
                "dewpoint" in name
                or "dew_point" in name
                or "dew point" in name
            ):
                dewpoint_col = original

        # Check relationship only if both columns exist

        if temperature_col and dewpoint_col:

            try:

                correlation_matrix = df[
                    [temperature_col, dewpoint_col]
                ].corr()

                corr_value = correlation_matrix.iloc[0, 1]

                # Very strong relationship
                if abs(corr_value) >= 0.80:

                    overlap_warnings.append(
                        f"{temperature_col} and {dewpoint_col} "
                        f"show a very strong relationship "
                        f"(Pearson r = {corr_value:.3f}). "
                        "These variables may contain overlapping "
                        "information and could introduce redundancy "
                        "in predictive models."
                    )

                    findings.extend(
                        overlap_warnings
                    )

                    state.add_log(
                        "[Statistical Agent] Potential information "
                        "overlap detected between Temperature and DewPoint."
                    )

            except Exception:

                pass

        # ---------------------------------------------------------
        # 6. Normality Analysis
        # ---------------------------------------------------------

        non_normal = []

        if isinstance(normality, dict):

            for variable, result in normality.items():

                if not isinstance(result, dict):
                    continue

                approximately_normal = result.get(
                    "approximately_normal_at_0.05",
                    False
                )

                if not approximately_normal:

                    non_normal.append(variable)

        if non_normal:

            findings.append(
                "Some numerical variables may deviate "
                "from a normal distribution at the 0.05 "
                "significance level."
            )

            findings.append(
                "Variables requiring attention: "
                + ", ".join(non_normal)
                + "."
            )

        else:

            findings.append(
                "The tested numerical variables were not "
                "flagged as significantly non-normal at the "
                "0.05 significance level."
            )

        # ---------------------------------------------------------
        # 7. Save Statistical Results
        # ---------------------------------------------------------

        state.statistical_results = {

            "correlations": correlations,

            "normality": normality,

            "numeric_variables": numeric_columns,

            "findings": findings,

            "top_relationships": [

                {
                    "variable_1": a,
                    "variable_2": b,
                    "pearson_r": round(value, 4)
                }

                for a, b, value in strongest
            ],

            "non_normal_variables": non_normal,

            # NEW
            "overlap_warnings": overlap_warnings
        }

        # ---------------------------------------------------------
        # 8. Completion Log
        # ---------------------------------------------------------

        state.add_log(
            "[Statistical Agent] Statistical relationships "
            "and distributional assumptions assessed."
        )

        return state
