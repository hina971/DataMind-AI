
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

def choose_target(df, requested=None):
    if requested and requested in df.columns:
        return requested
    numeric = df.select_dtypes(include=np.number).columns.tolist()
    return numeric[0] if numeric else None

def regression_models(df, target):
    data = df.copy()
    data = data.dropna(subset=[target])
    if len(data) < 30:
        return {"status":"INSUFFICIENT_DATA","message":"Fewer than 30 usable rows."}

    X = data.drop(columns=[target])
    y = data[target]

    # Avoid raw datetime in baseline ML; derive useful calendar features.
    for c in list(X.select_dtypes(include=["datetime64[ns]","datetime64[ns, UTC]"]).columns):
        X[c+"_year"] = X[c].dt.year
        X[c+"_month"] = X[c].dt.month
        X[c+"_dayofyear"] = X[c].dt.dayofyear
        X.drop(columns=[c], inplace=True)

    numeric = X.select_dtypes(include=np.number).columns.tolist()
    categorical = X.select_dtypes(exclude=np.number).columns.tolist()

    transformers = []
    if numeric:
        transformers.append(("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]), numeric))
    if categorical:
        transformers.append(("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical))

    prep = ColumnTransformer(transformers)
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.2,random_state=42)

    models = {
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    }
    results = {}
    best_name, best_rmse = None, float("inf")
    best_pred = None

    for name, model in models.items():
        pipe = Pipeline([("preprocess", prep),("model",model)])
        pipe.fit(X_train,y_train)
        pred = pipe.predict(X_test)
        mae = mean_absolute_error(y_test,pred)
        rmse = float(np.sqrt(mean_squared_error(y_test,pred)))
        r2 = r2_score(y_test,pred)
        results[name] = {"MAE":round(float(mae),4),"RMSE":round(rmse,4),"R2":round(float(r2),4)}
        if rmse < best_rmse:
            best_rmse, best_name, best_pred = rmse, name, pred

    return {
        "status":"OK",
        "problem_type":"regression",
        "target":target,
        "rows_used":len(data),
        "test_size":len(y_test),
        "models":results,
        "best_model":best_name,
        "selection_metric":"RMSE (lower is better)"
    }
