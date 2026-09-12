
import numpy as np
import pandas as pd

def profile_dataset(df):
    numeric = df.select_dtypes(include=np.number).columns.tolist()
    categorical = df.select_dtypes(include=["object","category","bool"]).columns.tolist()
    datetime = df.select_dtypes(include=["datetime64[ns]","datetime64[ns, UTC]"]).columns.tolist()
    missing = df.isna().sum()
    missing_detail = {
        col: {"count": int(n), "percent": round(float(n/len(df)*100), 2)}
        for col,n in missing.items() if n > 0
    }
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "numeric_columns": numeric,
        "categorical_columns": categorical,
        "datetime_columns": datetime,
        "missing_cells": int(df.isna().sum().sum()),
        "missing_by_column": missing_detail,
        "duplicate_rows": int(df.duplicated().sum()),
        "constant_columns": [c for c in df.columns if df[c].nunique(dropna=False) <= 1],
    }

def detect_outliers(df):
    numeric = df.select_dtypes(include=np.number)
    result = {}
    for col in numeric.columns:
        s = numeric[col].dropna()
        if len(s) < 4:
            continue
        q1, q3 = s.quantile(.25), s.quantile(.75)
        iqr = q3-q1
        if iqr == 0:
            count = 0
        else:
            count = int(((s < q1-1.5*iqr) | (s > q3+1.5*iqr)).sum())
        result[col] = {"iqr_outliers": count, "outlier_percent": round(count/len(s)*100,2)}
    return result
