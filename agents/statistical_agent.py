if state.statistical_results:

    stats = state.statistical_results

    with st.expander(
        "📈 Statistical Analysis",
        expanded=True
    ):

        st.markdown(
            """
            ### Statistical Overview

            The Statistical Agent examined the numerical
            variables to understand relationships between variables
            and assess their distributional characteristics.

            **Pearson correlation** measures the strength and direction
            of linear relationships between numerical variables.

            **Normality assessment** helps determine whether variables
            approximately follow a normal distribution.
            """
        )

        findings = stats.get(
            "findings",
            []
        )

        if findings:

            st.markdown(
                "#### 📊 Key Statistical Findings"
            )

            for finding in findings:

                st.write(
                    "• " + finding
                )

        top_relationships = stats.get(
            "top_relationships",
            []
        )

        if top_relationships:

            st.markdown(
                "#### 🔗 Strongest Relationships"
            )

            for relationship in top_relationships:

                st.write(
                    f"**{relationship['variable_1']} ↔ "
                    f"{relationship['variable_2']}**  "
                    f"(Pearson r = "
                    f"{relationship['pearson_r']:.3f})"
                )

        non_normal = stats.get(
            "non_normal_variables",
            []
        )

        if non_normal:

            st.warning(
                "Some variables may not follow a normal "
                "distribution: "
                + ", ".join(non_normal)
            )

        else:

            st.success(
                "No tested variables were flagged as "
                "significantly non-normal."
            )
