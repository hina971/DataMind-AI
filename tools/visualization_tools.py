
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def generate_figures(df, quality, outdir="outputs/figures"):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    paths=[]

    numeric=df.select_dtypes(include=np.number)
    if numeric.shape[1] >= 2:
        ax = numeric.corr().style # ensure computation
        plt.figure(figsize=(9,7))
        plt.imshow(numeric.corr(), aspect="auto")
        plt.xticks(range(len(numeric.columns)), numeric.columns, rotation=75, ha="right")
        plt.yticks(range(len(numeric.columns)), numeric.columns)
        plt.title("Correlation Heatmap")
        plt.colorbar()
        plt.tight_layout()
        p=out/"correlation_heatmap.png"; plt.savefig(p,dpi=150); plt.close()
        paths.append(str(p))

    if len(numeric.columns):
        cols=numeric.columns[:6]
        n=len(cols)
        fig,axes=plt.subplots(n,1,figsize=(9,max(3*n,4)))
        if n==1: axes=[axes]
        for ax,col in zip(axes,cols):
            ax.hist(df[col].dropna(), bins=25)
            ax.set_title(f"Distribution: {col}")
            ax.set_xlabel(col); ax.set_ylabel("Frequency")
        fig.tight_layout()
        p=out/"numeric_distributions.png"; fig.savefig(p,dpi=150); plt.close(fig)
        paths.append(str(p))

    if quality.get("missing_by_column"):
        miss=quality["missing_by_column"]
        plt.figure(figsize=(9,4))
        plt.bar(miss.keys(), [v["percent"] for v in miss.values()])
        plt.xticks(rotation=70,ha="right")
        plt.ylabel("Missing (%)"); plt.title("Missing Values by Column")
        plt.tight_layout()
        p=out/"missing_values.png"; plt.savefig(p,dpi=150); plt.close()
        paths.append(str(p))

    return paths
