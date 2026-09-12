
import pandas as pd

def load_dataframe(source):
    name = getattr(source, "name", "").lower()
    if name.endswith(".csv"):
        return pd.read_csv(source)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(source)
    raise ValueError("Unsupported file type. Use CSV or Excel.")
