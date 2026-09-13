import streamlit as st
import pandas as pd
from pathlib import Path

from core.data_loader import load_dataframe
from core.analysis_state import AnalysisState
from agents.orchestrator_agent import OrchestratorAgent


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="DataMind AI",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# PROFESSIONAL HEADER
# =========================================================

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #1e3a8a, #2563eb, #0f766e);
        padding: 28px 30px;
        border-radius: 16px;
        margin-bottom: 22px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    ">
        <div style="
            color: white;
            font-size: 38px;
            font-weight: 800;
            letter-spacing: 0.5px;
        ">
            🧠 DataMind AI
        </div>

        <div style="
            color: #dbeafe;
            font-size: 17px;
            margin-top: 7px;
            font-weight: 500;
        ">
            Autonomous Multi-Agent Data Science Assistant
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📂 Dataset")

    uploaded = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"]
    )

    st.info(
        "DataMind AI uses specialized agents for "
        "data quality, statistics, machine learning, "
        "visualization and reliability review."
    )


# =========================================================
# LOAD DATASET
# =========================================================

if uploaded:

    try:

        df = load_dataframe(uploaded)

        st.session_state["df"] = df

        st.success(
            f"Loaded {len(df):,} rows × {len(df.columns)} columns"
        )

    except Exception as e:

        st.error(
            f"Could not load dataset: {e}"
        )

        st.stop()


elif "df" not in st.session_state:

    sample = Path(
        "data/simulated_weather.xlsx"
    )

    if sample.exists():

        st.session_state["df"] = pd.read_excel(
            sample
        )

        st.info(
            "Using the included sample weather dataset."
        )

    else:

        st.warning(
            "Upload a dataset to begin."
        )

        st.stop()


# =========================================================
# DATAFRAME
# =========================================================

df = st.session_state["df"]


# =========================================================
# DATASET PREVIEW
# =========================================================

with st.expander(
    "📋 Dataset Preview",
    expanded=True
):

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


# =========================================================
# USER REQUEST
# =========================================================

request = st.text_area(
    "What would you like DataMind AI to do?",
    value="Give me a complete analysis of this dataset.",
    height=100,
)


# =========================================================
# ANALYZE DATASET
# =========================================================

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

    log_box = st.empty()


    def log(msg):

        log_box.markdown(
            "### 🤖 Agent Activity\n"
            + "\n".join(
                f"- {x}"
                for x in state.activity_log
            )
        )


    state.log = log

    result = orchestrator.run(state)

    st.session_state["result"] = result


# =========================================================
# ANALYSIS RESULTS
# =========================================================

if "result" in st.session_state:

    state = st.session_state["result"]

    st.divider()

    st.header("📊 Analysis Results")


    # =====================================================
    # DATA QUALITY
    # =====================================================

    if state.quality_results:

        with st.expander(
            "🔍 Data Quality Analysis",
            expanded=True
        ):

            q = state.quality_results

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Rows",
                    f"{len(df):,}"
                )

            with col2:
                st.metric(
                    "Columns",
                    f"{len(df.columns):,}"
                )

            with col3:
                st.metric(
                    "Missing Cells",
                    f"{q.get('missing_cells', 0):,}"
                )

            with col4:
                st.metric(
                    "Duplicate Rows",
                    f"{q.get('duplicate_rows', 0):,}"
                )


            st.markdown("### 📌 Findings")

            findings = q.get(
                "findings",
                []
            )

            if findings:

                for finding in findings:
                    st.write(
                        f"• {finding}"
                    )

            else:

                st.info(
                    "No additional data-quality findings."
                )


            outliers = q.get(
                "outliers",
                {}
            )

            if outliers:

                st.markdown(
                    "### 📦 Outlier Assessment"
                )

                outlier_rows = []

                for column, info in outliers.items():

                    if isinstance(info, dict):

                        outlier_rows.append(
                            {
                                "Variable": column,
                                "IQR Outliers": info.get(
                                    "iqr_outliers",
                                    0
                                )
                            }
                        )

                if outlier_rows:

                    st.dataframe(
                        pd.DataFrame(
                            outlier_rows
                        ),
                        use_container_width=True,
                        hide_index=True
                    )


    # =====================================================
    # STATISTICAL ANALYSIS
    # =====================================================

    if state.statistical_results:

        with st.expander(
            "📈 Statistical Analysis",
            expanded=True
        ):

            stats = state.statistical_results

            st.markdown(
                "### 📌 Statistical Findings"
            )

            findings = stats.get(
                "findings",
                []
            )

            if findings:

                for finding in findings:

                    st.write(
                        f"• {finding}"
                    )

            else:

                st.info(
                    "No statistical findings available."
                )


            top_relationships = stats.get(
                "top_relationships",
                []
            )

            if top_relationships:

                st.markdown(
                    "### 🔗 Strongest Relationships"
                )

                relationship_rows = []

                for item in top_relationships:

                    relationship_rows.append(
                        {
                            "Variable 1": item.get(
                                "variable_1"
                            ),
                            "Variable 2": item.get(
                                "variable_2"
                            ),
                            "Pearson r": item.get(
                                "pearson_r"
                            )
                        }
                    )

                st.dataframe(
                    pd.DataFrame(
                        relationship_rows
                    ),
                    use_container_width=True,
                    hide_index=True
                )


            non_normal = stats.get(
                "non_normal_variables",
                []
            )

            if non_normal:

                st.markdown(
                    "### 📊 Distributional Assessment"
                )

                st.write(
                    "Variables showing evidence of "
                    "non-normality:"
                )

                st.write(
                    ", ".join(non_normal)
                )


            overlap = stats.get(
                "overlap_warnings",
                []
            )

            if overlap:

                st.markdown(
                    "### ⚠️ Information Overlap"
                )

                for warning in overlap:

                    st.warning(
                        warning
                    )


    # =====================================================
    # MACHINE LEARNING
    # =====================================================

    if state.ml_results:

        with st.expander(
            "🤖 Machine Learning Analysis",
            expanded=True
        ):

            ml = state.ml_results

            if ml.get("status") == "OK":

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Problem Type",
                        str(
                            ml.get(
                                "problem_type",
                                "Unknown"
                            )
                        ).title()
                    )

                with col2:

                    st.metric(
                        "Target",
                        str(
                            ml.get(
                                "target",
                                "Not identified"
                            )
                        )
                    )

                with col3:

                    st.metric(
                        "Best Model",
                        str(
                            ml.get(
                                "best_model",
                                "Not available"
                            )
                        )
                    )


                st.markdown(
                    "### 📊 Model Comparison"
                )

                models = ml.get(
                    "models",
                    {}
                )

                if models:

                    model_rows = []

                    for model_name, metrics in models.items():

                        row = {
                            "Model": model_name
                        }

                        if isinstance(metrics, dict):

                            for metric_name, value in metrics.items():

                                if isinstance(
                                    value,
                                    (int, float)
                                ):

                                    row[
                                        metric_name
                                    ] = round(
                                        value,
                                        4
                                    )

                        model_rows.append(row)


                    st.dataframe(
                        pd.DataFrame(
                            model_rows
                        ),
                        use_container_width=True,
                        hide_index=True
                    )

            else:

                st.warning(
                    ml.get(
                        "message",
                        "Machine-learning analysis "
                        "could not be completed."
                    )
                )


    # =====================================================
    # VISUALIZATIONS
    # =====================================================

    if state.visualization_results:

        with st.expander(
            "📉 Visualizations",
            expanded=True
        ):

            figures = state.visualization_results.get(
                "figures",
                []
            )

            if figures:

                for i in range(
                    0,
                    len(figures),
                    2
                ):

                    col1, col2 = st.columns(
                        2,
                        gap="medium"
                    )

                    with col1:

                        st.image(
                            figures[i],
                            width=400
                        )

                    if i + 1 < len(figures):

                        with col2:

                            st.image(
                                figures[i + 1],
                                width=400
                            )

            else:

                st.info(
                    "No visualization figures were generated."
                )


    # =====================================================
    # REVIEWER
    # =====================================================

    if state.reviewer_results:

        with st.expander(
            "🧐 Reliability Review",
            expanded=True
        ):

            review = state.reviewer_results

            reliability = review.get(
                "reliability",
                "UNKNOWN"
            )

            if reliability == "HIGH":

                st.success(
                    f"Reliability Assessment: {reliability}"
                )

            elif reliability == "MODERATE":

                st.warning(
                    f"Reliability Assessment: {reliability}"
                )

            else:

                st.error(
                    f"Reliability Assessment: {reliability}"
                )


            reason = review.get(
                "reason"
            )

            if reason:

                st.write(
                    reason
                )


            warnings = review.get(
                "warnings",
                []
            )

            if warnings:

                st.markdown(
                    "### ⚠️ Considerations"
                )

                for warning in warnings:

                    st.write(
                        f"• {warning}"
                    )

            else:

                st.success(
                    "No major concerns were identified."
                )


    # =====================================================
    # FINAL REPORT
    # =====================================================

    st.subheader(
        "📝 Final Report"
    )

    if state.final_report:

        st.markdown(
            state.final_report
        )

    else:

        st.info(
            "Final report is not available."
        )


# =========================================================
# PROFESSIONAL FOOTER
# =========================================================

st.markdown(
    """
    <div style="
        margin-top: 45px;
        padding: 28px 25px;
        border-radius: 16px;
        background: linear-gradient(135deg, #0f172a, #1e3a8a, #0f766e);
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    ">

        <div style="
            color: white;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: 0.4px;
        ">
            🧠 DataMind AI
        </div>

        <div style="
            color: #dbeafe;
            font-size: 15px;
            margin-top: 7px;
            font-weight: 500;
        ">
            Autonomous Multi-Agent Data Science Assistant
        </div>

        <div style="
            color: #e5e7eb;
            font-size: 14px;
            margin-top: 18px;
            line-height: 1.8;
        ">
            <strong>Developed by Hina Ramzan &amp; Team</strong>
            <br>
            Team Members:
            Hina Ramzan • Fayaz Ali • Nisha Shabbir •
            Moin Afzal • Talal Azhar
        </div>

        <div style="
            color: #94a3b8;
            font-size: 12px;
            margin-top: 18px;
        ">
            © 2026 DataMind AI Team
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
