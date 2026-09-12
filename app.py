import streamlit as st
import pandas as pd
from pathlib import Path
from core.data_loader import load_dataframe
from core.analysis_state import AnalysisState
from agents.orchestrator_agent import OrchestratorAgent


st.set_page_config(
    page_title="DataMind AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 DataMind AI")
st.caption("Autonomous Multi-Agent Data Science Assistant")


with st.sidebar:
    st.header("Dataset")

    uploaded = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"]
    )

    st.info(
        "The system uses specialized agents for quality, "
        "statistics, ML, visualization and review."
    )


if uploaded:
    try:
        df = load_dataframe(uploaded)

        st.session_state["df"] = df

        st.success(
            f"Loaded {len(df):,} rows × {len(df.columns)} columns"
        )

    except Exception as e:
        st.error(f"Could not load dataset: {e}")
        st.stop()


elif "df" not in st.session_state:

    sample = Path("data/simulated_weather.xlsx")

    if sample.exists():
        st.session_state["df"] = pd.read_excel(sample)

        st.info(
            "Using the included sample weather dataset."
        )

    else:
        st.warning("Upload a dataset to begin.")
        st.stop()


df = st.session_state["df"]


with st.expander("Dataset Preview", expanded=True):
    st.dataframe(
        df.head(10),
        use_container_width=True
    )


request = st.text_area(
    "What would you like DataMind AI to do?",
    value="Give me a complete analysis of this dataset.",
    height=100,
)


if st.button(
    "🚀 Analyze Dataset",
    type="primary",
    use_container_width=True
):

    state = AnalysisState(
        user_request=request,
        dataframe=df
    )

    orchestrator = OrchestratorAgent()

    progress = st.empty()
    log_box = st.empty()


    # Display agent activity
    # AnalysisState.add_log() already adds the message
    def log(msg):
        log_box.markdown(
            "### Agent Activity\n"
            + "\n".join(
                f"- {x}"
                for x in state.activity_log
            )
        )


    state.log = log

    result = orchestrator.run(state)

    st.session_state["result"] = result


if "result" in st.session_state:

    state = st.session_state["result"]

    st.divider()

    st.subheader("📊 Dataset Quality")

    q = state.quality_results

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Rows",
        q.get("rows", 0)
    )

    c2.metric(
        "Columns",
        q.get("columns", 0)
    )

    c3.metric(
        "Missing Cells",
        q.get("missing_cells", 0)
    )

    c4.metric(
        "Duplicates",
        q.get("duplicate_rows", 0)
    )


    
    with st.expander("🔍 Data Quality Details", expanded=True):

    st.markdown(
        f"""
        ### Dataset Quality Overview

        The dataset contains **{q.get("rows", 0):,} observations**
        and **{q.get("columns", 0)} variables**.

        The automated Data Quality Agent checked the dataset for
        missing values, duplicate records, constant variables,
        data types, and potential statistical outliers.
        """
    )

    # Missing values
    missing = q.get("missing_by_column", {})

    if missing:
        st.markdown("#### ⚠️ Missing Values")

        for column, info in missing.items():
            st.write(
                f"**{column}** contains "
                f"{info.get('count', 0)} missing values "
                f"({info.get('percent', 0):.2f}%)."
            )
    else:
        st.success("✅ No missing values were detected.")

    # Duplicates
    if q.get("duplicate_rows", 0) > 0:
        st.warning(
            f"⚠️ {q.get('duplicate_rows')} duplicate rows were detected."
        )
    else:
        st.success("✅ No duplicate rows were detected.")

    # Constant columns
    constants = q.get("constant_columns", [])

    if constants:
        st.warning(
            "Constant variables detected: "
            + ", ".join(constants)
        )

    # Outliers
    outliers = q.get("outliers", {})

    if outliers:

        st.markdown("#### 📌 Potential Outliers")

        found = False

        for column, info in outliers.items():

            count = info.get("iqr_outliers", 0)
            percent = info.get("outlier_percent", 0)

            if count > 0:
                found = True

                st.write(
                    f"**{column}**: {count:,} potential outliers "
                    f"({percent:.2f}% of available observations)."
                )

        if not found:
            st.success("✅ No IQR-based outliers were detected.")


    if state.statistical_results:

        with st.expander(
            "📈 Statistical Analysis",
            expanded=True
        ):
            st.json(
                state.statistical_results
            )


    if state.ml_results:

        with st.expander(
            "🤖 Machine Learning",
            expanded=True
        ):
            st.json(
                state.ml_results
            )


    if state.visualization_results:

        with st.expander(
            "📉 Visualizations",
            expanded=True
        ):

            for fig_path in state.visualization_results.get(
                "figures",
                []
            ):

                st.image(
                    fig_path,
                    use_container_width=True
                )


    with st.expander(
        "🛡️ Reviewer / Reliability",
        expanded=True
    ):
        st.json(
            state.reviewer_results
        )


    st.subheader("📝 Final Report")

    st.markdown(
        state.final_report
    )


# ============================================================
# FOOTER
# ============================================================

# Footer

st.divider()

st.markdown("### 🧠 DataMind AI")
st.write("Developed by Hina Ramzan & Team")
st.write("Team Members: Hina Ramzan • Fayaz Ali • Nisha shabbir • Moin Afzal • Abdul Samad • Talal Azhar ")
st.write("Autonomous Multi-Agent Data Science Assistant")
st.caption("© 2026 DataMind AI Team")
