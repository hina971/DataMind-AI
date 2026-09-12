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

        # Correlation analysis
        correlations = correlation_analysis(df)

        # Normality assessment
        normality = normality_summary(df)

        # Numerical variables
        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        findings = []

        findings.append(
            f"The dataset contains {len(numeric_columns)} "
            "numerical variables suitable for statistical analysis."
        )

        # --------------------------------------------------
        # Pearson Correlation Findings
        # --------------------------------------------------

        pearson = correlations.get(
            "pearson",
            {}
        )

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
                            sorted(
                                [variable, other]
                            )
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
                (
                    a,
                    b,
                    value
                )
                for (a, b), value
                in unique_relationships.items()
            ],
            key=lambda x: abs(x[2]),
            reverse=True
        )[:5]

        if strongest:

            findings.append(
                "The correlation analysis identified the "
                "strongest relationships between numerical variables."
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

        # --------------------------------------------------
        # Normality Findings
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Save Results
        # --------------------------------------------------

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

            "non_normal_variables": non_normal
        }

        state.add_log(
            "[Statistical Agent] Statistical relationships "
            "and distributional assumptions assessed."
        )

        return state
