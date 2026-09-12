
import numpy as np
from scipy import stats

def correlation_analysis(df):
    numeric = df.select_dtypes(include=np.number)
    if numeric.shape[1] < 2:
        return {"message": "At least two numeric variables are required."}
    pearson = numeric.corr(method="pearson").round(4)
    spearman = numeric.corr(method="spearman").round(4)
    return {
        "pearson": pearson.to_dict(),
        "spearman": spearman.to_dict()
    }

def normality_summary(df):
    numeric = df.select_dtypes(include=np.number)
    out = {}
    for col in numeric.columns:
        s = numeric[col].dropna()
        if 3 <= len(s) <= 5000:
            stat,p = stats.shapiro(s)
            out[col] = {"shapiro_stat": round(float(stat),4), "p_value": round(float(p),6),
                        "approximately_normal_at_0.05": bool(p >= 0.05)}
    return out
