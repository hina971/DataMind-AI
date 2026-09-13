import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components

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


# =========================================================
# DATAMIND AI — ANIMATED HEADER
# =========================================================

components.html(
    """
    <style>
        body {
            margin: 0;
            background: transparent;
            font-family: Arial, sans-serif;
        }

        .header-box {
            height: 205px;
            border-radius: 22px;

            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            text-align: center;

            background: linear-gradient(
                120deg,
                #172554,
                #1d4ed8,
                #2563eb,
                #0f766e,
                #172554
            );

            background-size: 400% 400%;
            animation: gradientAnimation 8s ease infinite;

            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        }

        .title {
            color: white;
            font-size: 42px;
            font-weight: 900;
            letter-spacing: 1px;

            animation: titlePulse 2.5s ease-in-out infinite;
        }

        .subtitle {
            color: #dbeafe;
            font-size: 17px;
            font-weight: 500;
            margin-top: 8px;
        }

        .badge {
            margin-top: 16px;
            padding: 7px 18px;
            border-radius: 30px;

            color: white;
            font-size: 13px;
            font-weight: 600;

            background: rgba(255,255,255,0.13);
            border: 1px solid rgba(255,255,255,0.25);
        }

        @keyframes gradientAnimation {
            0% {
                background-position: 0% 50%;
            }

            50% {
                background-position: 100% 50%;
            }

            100% {
                background-position: 0% 50%;
            }
        }

        @keyframes titlePulse {
            0%, 100% {
                transform: scale(1);
                text-shadow:
                    0 0 5px rgba(255,255,255,0.2);
            }

            50% {
                transform: scale(1.04);
                text-shadow:
                    0 0 12px rgba(255,255,255,0.7),
                    0 0 30px rgba(147,197,253,0.7);
            }
        }
    </style>

    <div class="header-box">

        <div class="title">
            🧠 DataMind AI
        </div>

        <div class="subtitle">
            Autonomous Multi-Agent Data Science Assistant
        </div>

        <div class="badge">
            ✨ Intelligent • Autonomous • Data-Driven
        </div>

    </div>
    """,
    height=225,
    scrolling=False
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
    # Agent Activity Display
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
    # Run Orchestrator
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


                # Remove duplicate pairs

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

                # ------------------------------------------------
                # Two Visualizations Per Row
                # ------------------------------------------------

                for i in range(
                    0,
                    len(figures),
                    2
                ):

                    col1, col2 = st.columns(
                        2,
                        gap="medium"
                    )


                    # First figure

                    with col1:

                        st.image(
                            figures[i],
                            width=400
                        )


                    # Second figure

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

st.divider()


footer_left, footer_center, footer_right = st.columns(
    [1, 3, 1]
)

with footer_center:

    st.markdown(
        """
        ## 🧠 DataMind AI
        """,
        unsafe_allow_html=False
    )

    st.caption(
        "Autonomous Multi-Agent Data Science Assistant"
    )

    st.write(
        "**Developed by Hina Ramzan & Team**"
    )

    st.write(
        "Team Members: Hina Ramzan • Fayaz Ali • "
        "Nisha Shabbir • Moin Afzal • "
        "Abdul Samad • Talal Azhar"
    )

    st.caption(
        "© 2026 DataMind AI Team"
    )
