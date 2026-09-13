# ============================================================
# VISUALIZATIONS
# ============================================================

st.subheader("📉 Visualizations")

if state.visualization_results:

    figures = state.visualization_results.get("figures", [])

    if figures:

        # Show 2 graphs in each row
        for i in range(0, len(figures), 2):

            col1, col2 = st.columns(2)

            # First graph
            with col1:
                st.image(
                    figures[i],
                    width=300
                )

            # Second graph
            if i + 1 < len(figures):
                with col2:
                    st.image(
                        figures[i + 1],
                        width=300
                    )

    else:
        st.info("No visualizations were generated.")

else:
    st.info("No visualizations available.")
