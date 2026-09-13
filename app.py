import streamlit as st
import pandas as pd
from pathlib import Path

from core.data_loader import load_dataframe
from core.analysis_state import AnalysisState
from agents.orchestrator_agent import OrchestratorAgent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DataMind AI",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Header ---------- */

    .datamind-header {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #1e3a8a 50%,
            #2563eb 100%
        );

        padding: 30px 20px;
        border-radius: 20px;

        text-align: center;

        margin-top: 10px;
        margin-bottom: 25px;

        box-shadow:
            0 8px 25px rgba(30, 64, 175, 0.25);
    }


    .datamind-title {
        color: white;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 6px;
    }


    .datamind-subtitle {
        color: #dbeafe;
        font-size: 17px;
        font-weight: 400;
    }


    /* ---------- Footer ---------- */

    .datamind-footer {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #172554 50%,
            #1e40af 100%
        );

        padding: 28px 20px;
        border-radius: 20px;

        text-align: center;

        margin-top: 35px;
        margin-bottom: 10px;

        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.25);
    }


    .datamind-footer-title {
        color: white;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 5px;
    }


    .datamind-footer-subtitle {
        color: #dbeafe;
        font-size: 15px;
        margin-bottom: 15px;
    }


    .datamind-footer-team {
        color: #e5e7eb;
        font-size: 14px;
        line-height: 1.7;
    }


    .datamind-footer-copy {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="datamind-header">
        <div class="datamind-title">
            🧠 DataMind AI
        </div>

        <div class="datamind-subtitle">
            Autonomous Multi-Agent Data Science Assistant
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Dataset")

    uploaded = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"]
    )

    st.info(
        "The system uses specialized agents for "
        "quality, statistics, machine learning, "
        "visualization and reliability review."
    )


# ============================================================
# DATA LOADING
# ============================================================

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


df = st.session_state["df"]


# ============================================================
# DATASET PREVIEW
# ============================================================

with st.expander(
    "📋 Dataset Preview",
    expanded=True
):

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


# ============================================================
# USER REQUEST
# ============================================================

request = st.text_area(
    "What would you like DataMind AI to do?",
    value="Give me a complete analysis of this dataset.",
    height=100,
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

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


    # --------------------------------------------------------
    # AGENT ACTIVITY
    # --------------------------------------------------------

    def log(msg):

        log_box.markdown(
            "### 🤖 Agent Activity\n"
            + "\n".join(
                f"- {x}"
                for x in state.activity_log
            )
        )

    state.log = log


    # --------------------------------------------------------
    # RUN ORCHESTRATOR
    # --------------------------------------------------------

    result = orchestrator.run(state)

    st.session_state["result"] = result


# ============================================================
# RESULTS
# ============================================================

if "result" in st.session_state:

    state = st.session_state["result"]

    st.divider()

    st.header("📊 Analysis Results")


    # ========================================================
    # DATA QUALITY
    # ========================================================

    st.subheader("🔍 Dataset Quality")

    q = state.quality_results or {}

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


    # ========================================================
    # DATA QUALITY DETAILS
    # ========================================================

    with st.expander(
        "🔍 Data Quality Details",
        expanded=True
    ):

        st.markdown(
            f"""
            ### Dataset Quality Overview

            The dataset contains **{q.get("rows", 0):,} observations**
            and **{q.get("columns", 0)} variables**.

            The automated Data Quality Agent examined the dataset
            for missing values, duplicate records, constant
            variables, variable types and potential statistical
            outliers.
            """
        )


        # ----------------------------------------------------
        # Missing Values
        # ----------------------------------------------------

        missing = q.get(
            "missing_by_column",
            {}
        )

        if missing:

            st.markdown(
                "#### ⚠️ Missing Values"
            )

            for column, info in missing.items():

                st.write(
                    f"**{column}** contains "
                    f"{info.get('count', 0)} missing values "
                    f"({info.get('percent', 0):.2f}%)."
                )

        else:

            st.success(
                "✅ No missing values were detected."
            )


        # ----------------------------------------------------
        # Duplicate Rows
        # ----------------------------------------------------

        if q.get(
            "duplicate_rows",
            0
        ) > 0:

            st.warning(
                f"⚠️ {q.get('duplicate_rows'):,} "
                f"duplicate rows were detected."
            )

        else:

            st.success(
                "✅ No duplicate rows were detected."
            )


        # ----------------------------------------------------
        # Constant Columns
        # ----------------------------------------------------

        constants = q.get(
            "constant_columns",
            []
        )

        if constants:

            st.warning(
                "Constant variables detected: "
                + ", ".join(constants)
            )

        else:

            st.success(
                "✅ No constant variables were detected."
            )


        # ----------------------------------------------------
        # Outliers
        # ----------------------------------------------------

        outliers = q.get(
            "outliers",
            {}
        )

        st.markdown(
            "#### 📌 Potential Outliers"
        )

        found = False

        for column, info in outliers.items():

            count = info.get(
                "iqr_outliers",
                0
            )

            percent = info.get(
                "outlier_percent",
                0
            )

            if count > 0:

                found = True

                st.write(
                    f"**{column}**: "
                    f"{count:,} potential outliers "
                    f"({percent:.2f}% of available observations)."
                )

        if not found:

            st.success(
                "✅ No IQR-based outliers were detected."
            )


    # ========================================================
    # STATISTICAL ANALYSIS
    # ========================================================

    if state.statistical_results:

        stats = state.statistical_results

        with st.expander(
            "📈 Statistical Analysis",
            expanded=True
        ):

            st.markdown(
                """
                ### Statistical Overview

                The Statistical Agent examined numerical variables
                to identify relationships between variables and
                assess their distributional characteristics.

                **Pearson correlation** measures linear relationships,
                while **Spearman correlation** evaluates monotonic
                relationships.

                A normality assessment was also performed where
                applicable to identify variables whose distributions
                may differ from normality.
                """
            )


            # ------------------------------------------------
            # Correlations
            # ------------------------------------------------

            pearson = stats.get(
                "correlations",
                {}
            ).get(
                "pearson",
                {}
            )

            if pearson:

                st.markdown(
                    "#### 🔗 Strongest Relationships"
                )

                relationships = []

                for variable, values in pearson.items():

                    if not isinstance(
                        values,
                        dict
                    ):
                        continue

                    for other, value in values.items():

                        if variable == other:
                            continue

                        try:

                            relationships.append(
                                (
                                    variable,
                                    other,
                                    float(value)
                                )
                            )

                        except (
                            TypeError,
                            ValueError
                        ):

                            continue


                unique = {}

                for a, b, value in relationships:

                    key = tuple(
                        sorted(
                            [a, b]
                        )
                    )

                    if key not in unique:

                        unique[key] = value


                strongest = sorted(
                    [
                        (
                            a,
                            b,
                            value
                        )
                        for (
                            a,
                            b
                        ), value in unique.items()
                    ],
                    key=lambda x: abs(x[2]),
                    reverse=True
                )[:5]


                for a, b, value in strongest:

                    if abs(value) >= 0.7:

                        strength = "strong"

                    elif abs(value) >= 0.4:

                        strength = "moderate"

                    else:

                        strength = "weak"


                    if value > 0:

                        direction = "positive"

                    elif value < 0:

                        direction = "negative"

                    else:

                        direction = "negligible"


                    st.write(
                        f"**{a} ↔ {b}** shows a "
                        f"{strength} {direction} relationship "
                        f"(Pearson r = {value:.3f})."
                    )


                # ------------------------------------------------
                # Information Overlap
                # ------------------------------------------------

                overlap_warnings = stats.get(
                    "overlap_warnings",
                    []
                )

                if overlap_warnings:

                    st.markdown(
                        "#### ⚠️ Potential Information Overlap"
                    )

                    for warning in overlap_warnings:

                        st.warning(
                            warning
                        )


            # ------------------------------------------------
            # Normality
            # ------------------------------------------------

            normality = stats.get(
                "normality",
                {}
            )

            if normality:

                st.markdown(
                    "#### 📐 Distribution Assessment"
                )

                non_normal = [
                    variable
                    for variable, result
                    in normality.items()
                    if not result.get(
                        "approximately_normal_at_0.05",
                        False
                    )
                ]

                if non_normal:

                    st.warning(
                        "Some numerical variables may not "
                        "follow a normal distribution at the "
                        "0.05 significance level."
                    )

                    st.write(
                        "**Variables requiring attention:** "
                        + ", ".join(non_normal)
                    )

                else:

                    st.success(
                        "No tested variables were flagged "
                        "as significantly non-normal."
                    )


    # ========================================================
    # MACHINE LEARNING
    # ========================================================

    if state.ml_results:

        ml = state.ml_results

        with st.expander(
            "🤖 Machine Learning",
            expanded=True
        ):

            problem_type = ml.get(
                "problem_type",
                "unknown"
            )

            target = ml.get(
                "target",
                "not specified"
            )

            best_model = ml.get(
                "best_model",
                "not specified"
            )


            st.markdown(
                f"""
                ### Machine Learning Overview

                The ML Agent automatically identified the task as
                a **{problem_type}** problem.

                The selected prediction target is
                **{target}**.

                Multiple baseline machine-learning models were
                evaluated and compared using appropriate
                performance metrics.

                The current best-performing model is
                **{best_model}**.
                """
            )


            # ------------------------------------------------
            # Model Comparison
            # ------------------------------------------------

            models = ml.get(
                "models",
                {}
            )

            if models:

                st.markdown(
                    "#### 🧠 Model Comparison"
                )

                for model_name, metrics in models.items():

                    st.markdown(
                        f"**{model_name}**"
                    )

                    if isinstance(
                        metrics,
                        dict
                    ):

                        metric_text = []

                        for metric_name, value in metrics.items():

                            try:

                                metric_text.append(
                                    f"{metric_name}: {float(value):.4f}"
                                )

                            except (
                                TypeError,
                                ValueError
                            ):

                                metric_text.append(
                                    f"{metric_name}: {value}"
                                )

                        st.write(
                            " | ".join(metric_text)
                        )


            st.info(
                "These results represent a baseline evaluation. "
                "For research-grade modelling, cross-validation, "
                "feature engineering and further model tuning "
                "are recommended."
            )


    # ========================================================
    # VISUALIZATIONS
    # ========================================================

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


    # ========================================================
    # REVIEWER
    # ========================================================

    with st.expander(
        "🛡️ Reviewer / Reliability",
        expanded=True
    ):

        review = state.reviewer_results or {}

        reliability = review.get(
            "reliability",
            "UNKNOWN"
        )

        reason = review.get(
            "reason",
            ""
        )

        st.markdown(
            f"""
            ### Reliability Assessment

            **Overall Reliability: {reliability}**

            {reason}
            """
        )


        warnings = review.get(
            "warnings",
            []
        )

        if warnings:

            st.markdown(
                "#### ⚠️ Important Considerations"
            )

            for warning in warnings:

                st.warning(
                    warning
                )

        else:

            st.success(
                "✅ No major reliability warnings were identified."
            )


    # ========================================================
    # FINAL REPORT
    # ========================================================

    st.subheader(
        "📝 Final Report"
    )

    st.markdown(
        state.final_report
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")


footer_left, footer_center, footer_right = st.columns(
    [1, 3, 1]
)

with footer_center:

    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0f172a, #1e3a8a, #2563eb);
            padding: 28px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(30,64,175,0.25);
        ">

            <div style="
                color: white;
                font-size: 28px;
                font-weight: 800;
            ">
                🧠 DataMind AI
            </div>

            <div style="
                color: #dbeafe;
                font-size: 15px;
                margin-top: 6px;
            ">
                Autonomous Multi-Agent Data Science Assistant
            </div>

            <div style="
                color: #e5e7eb;
                font-size: 14px;
                margin-top: 18px;
                line-height: 1.7;
            ">
                <b>Developed by Hina Ramzan & Team</b>
                <br><br>
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
