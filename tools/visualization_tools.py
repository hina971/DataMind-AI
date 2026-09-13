import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


OUTPUT_DIR = "outputs/figures"


def ensure_output_dir():
    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


# ==========================================================
# 1. CORRELATION HEATMAP
# ==========================================================

def create_correlation_heatmap(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    if numeric.shape[1] < 2:
        return None

    ensure_output_dir()

    fig, ax = plt.subplots(
        figsize=(6, 4)
    )

    correlation = numeric.corr()

    image = ax.imshow(
        correlation,
        aspect="auto"
    )

    ax.set_xticks(
        range(len(correlation.columns))
    )

    ax.set_yticks(
        range(len(correlation.columns))
    )

    ax.set_xticklabels(
        correlation.columns,
        rotation=90,
        fontsize=7
    )

    ax.set_yticklabels(
        correlation.columns,
        fontsize=7
    )

    fig.colorbar(
        image,
        ax=ax
    )

    ax.set_title(
        "Correlation Heatmap",
        fontsize=10
    )

    fig.tight_layout()

    path = os.path.join(
        OUTPUT_DIR,
        "correlation_heatmap.png"
    )

    fig.savefig(
        path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

    return path


# ==========================================================
# 2. VARIABLE DISTRIBUTIONS
# ==========================================================

def create_distributions(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    if numeric.empty:
        return []

    ensure_output_dir()

    figures = []

    for column in numeric.columns:

        fig, ax = plt.subplots(
            figsize=(5, 3.2)
        )

        ax.hist(
            numeric[column].dropna(),
            bins=30
        )

        ax.set_title(
            f"Distribution of {column}",
            fontsize=9
        )

        ax.set_xlabel(
            column,
            fontsize=8
        )

        ax.set_ylabel(
            "Frequency",
            fontsize=8
        )

        ax.tick_params(
            axis="both",
            labelsize=7
        )

        fig.tight_layout()

        safe_name = (
            str(column)
            .replace(" ", "_")
            .replace("/", "_")
        )

        path = os.path.join(
            OUTPUT_DIR,
            f"distribution_{safe_name}.png"
        )

        fig.savefig(
            path,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close(fig)

        figures.append(path)

    return figures


# ==========================================================
# 3. OUTLIER BOXPLOTS
# ==========================================================

def create_boxplots(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    if numeric.empty:
        return []

    ensure_output_dir()

    figures = []

    for column in numeric.columns:

        fig, ax = plt.subplots(
            figsize=(5, 3.2)
        )

        ax.boxplot(
            numeric[column].dropna()
        )

        ax.set_title(
            f"Outlier Boxplot — {column}",
            fontsize=9
        )

        ax.set_ylabel(
            column,
            fontsize=8
        )

        ax.tick_params(
            axis="both",
            labelsize=7
        )

        fig.tight_layout()

        safe_name = (
            str(column)
            .replace(" ", "_")
            .replace("/", "_")
        )

        path = os.path.join(
            OUTPUT_DIR,
            f"boxplot_{safe_name}.png"
        )

        fig.savefig(
            path,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close(fig)

        figures.append(path)

    return figures


# ==========================================================
# 4. MISSING VALUE CHART
# ==========================================================

def create_missing_values_chart(df):

    missing = (
        df.isnull()
        .sum()
    )

    missing = missing[
        missing > 0
    ]

    if missing.empty:
        return None

    ensure_output_dir()

    fig, ax = plt.subplots(
        figsize=(6, 3.5)
    )

    ax.bar(
        missing.index.astype(str),
        missing.values
    )

    ax.set_title(
        "Missing Values by Variable",
        fontsize=10
    )

    ax.set_xlabel(
        "Variable",
        fontsize=8
    )

    ax.set_ylabel(
        "Missing Count",
        fontsize=8
    )

    ax.tick_params(
        axis="x",
        rotation=45,
        labelsize=7
    )

    ax.tick_params(
        axis="y",
        labelsize=7
    )

    fig.tight_layout()

    path = os.path.join(
        OUTPUT_DIR,
        "missing_values.png"
    )

    fig.savefig(
        path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

    return path


# ==========================================================
# 5. MODEL PERFORMANCE
# ==========================================================

def create_model_performance_plot(
    ml_results
):

    if not ml_results:
        return None

    models = ml_results.get(
        "models",
        {}
    )

    if not models:
        return None

    problem_type = ml_results.get(
        "problem_type",
        ""
    )

    ensure_output_dir()

    names = list(
        models.keys()
    )

    fig, ax = plt.subplots(
        figsize=(6, 3.5)
    )

    if problem_type == "classification":

        scores = [
            models[name].get(
                "F1",
                0
            )
            for name in names
        ]

        ax.bar(
            names,
            scores
        )

        ax.set_ylabel(
            "Weighted F1 Score",
            fontsize=8
        )

        ax.set_title(
            "Classification Model Performance",
            fontsize=10
        )

    else:

        scores = [
            models[name].get(
                "RMSE",
                0
            )
            for name in names
        ]

        ax.bar(
            names,
            scores
        )

        ax.set_ylabel(
            "RMSE",
            fontsize=8
        )

        ax.set_title(
            "Regression Model Performance",
            fontsize=10
        )

    ax.tick_params(
        axis="x",
        rotation=30,
        labelsize=7
    )

    ax.tick_params(
        axis="y",
        labelsize=7
    )

    fig.tight_layout()

    path = os.path.join(
        OUTPUT_DIR,
        "model_performance.png"
    )

    fig.savefig(
        path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

    return path


# ==========================================================
# 6. MAIN VISUALIZATION FUNCTION
# ==========================================================

def generate_visualizations(
    df,
    ml_results=None
):

    ensure_output_dir()

    figures = []

    # Correlation
    heatmap = create_correlation_heatmap(
        df
    )

    if heatmap:
        figures.append(
            heatmap
        )

    # Distributions
    figures.extend(
        create_distributions(df)
    )

    # Boxplots
    figures.extend(
        create_boxplots(df)
    )

    # Missing values
    missing_chart = (
        create_missing_values_chart(df)
    )

    if missing_chart:
        figures.append(
            missing_chart
        )

    # ML model performance
    if ml_results:

        performance = (
            create_model_performance_plot(
                ml_results
            )
        )

        if performance:
            figures.append(
                performance
            )

    return {
        "figures": figures,
        "total_figures": len(figures)
    }
