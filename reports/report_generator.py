
from datetime import datetime

def generate_report(state):
    q=state.quality_results
    r=state.reviewer_results
    lines=[]
    lines.append("# DataMind AI Analytical Report")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("\n## Executive Summary")
    lines.append(
        f"The dataset contains **{q.get('rows',0):,} rows** and **{q.get('columns',0)} columns**. "
        f"The automated pipeline inspected data quality and executed the analyses requested by the user."
    )
    lines.append("\n## Dataset Overview")
    lines.append(f"- Numeric variables: {len(q.get('numeric_columns',[]))}")
    lines.append(f"- Categorical variables: {len(q.get('categorical_columns',[]))}")
    lines.append(f"- Datetime variables: {len(q.get('datetime_columns',[]))}")
    lines.append(f"- Missing cells: {q.get('missing_cells',0)}")
    lines.append(f"- Duplicate rows: {q.get('duplicate_rows',0)}")

    lines.append("\n## Data Quality")
    if q.get("missing_by_column"):
        lines.append("Missing values were detected in: " + ", ".join(q["missing_by_column"].keys()) + ".")
    else:
        lines.append("No missing values were detected.")
    outliers=[c for c,v in q.get("outliers",{}).items() if v.get("iqr_outliers",0)>0]
    lines.append("IQR outliers detected in: " + (", ".join(outliers) if outliers else "none") + ".")

    if state.statistical_results:
        lines.append("\n## Statistical Analysis")
        lines.append("Correlation matrices and Shapiro normality summaries were computed where applicable.")
        lines.append("The raw structured results are available in the Statistical Analysis panel.")

    if state.ml_results:
        lines.append("\n## Machine Learning")
        m=state.ml_results
        if m.get("status")=="OK":
            lines.append(f"- Problem type: {m.get('problem_type')}")
            lines.append(f"- Target: **{m.get('target')}**")
            lines.append(f"- Best baseline model: **{m.get('best_model')}**")
            lines.append(f"- Selection metric: {m.get('selection_metric')}")
        else:
            lines.append(m.get("message","ML was not performed."))

    lines.append("\n## Reliability Review")
    lines.append(f"**{r.get('reliability','UNKNOWN')}** — {r.get('reason','')}")
    for w in r.get("warnings",[]):
        lines.append(f"- {w}")

    lines.append("\n## Final Recommendations")
    lines.append("- Review detected quality issues before making high-stakes conclusions.")
    lines.append("- Treat automated ML results as a baseline rather than a final production model.")
    lines.append("- For research-grade inference, verify assumptions and use domain knowledge.")
    return "\n".join(lines)
