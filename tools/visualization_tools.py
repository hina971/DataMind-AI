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
        figsize=(10, 7)
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
        rotation=90
    )

    ax.set_yticklabels(
        correlation.columns
    )

    fig.colorbar(
        image,
        ax=ax
    )

    ax.set_title(
        "Correlation Heatmap"
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

    # Plot ALL numerical variables
    for column in numeric.columns:

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.hist(
            numeric[column].dropna(),
            bins=30
        )

        ax.set_title(
            f"Distribution of {column}"
        )

        ax.set_xlabel(
            column
        )

        ax.set_ylabel(
            "Frequency"
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
            figsize=(8, 5)
        )

        ax.boxplot(
            numeric[column].dropna()
        )

        ax.set_title(
            f"Outlier Boxplot — {column}"
        )

        ax.set_ylabel(
            column
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
        figsize=(10, 5)
    )

    ax.bar(
        missing.index.astype(str),
        missing.values
    )

    ax.set_title(
        "Missing Values by Variable"
    )

    ax.set_xlabel(
        "Variable"
    )

    ax.set_ylabel(
        "Missing Count"
    )

    ax.tick_params(
        axis="x",
        rotation=45
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
        figsize=(10, 6)
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
            "Weighted F1 Score"
        )

        ax.set_title(
            "Classification Model Performance"
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
            "RMSE"
        )

        ax.set_title(
            "Regression Model Performance"
        )

    ax.tick_params(
        axis="x",
        rotation=30
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
