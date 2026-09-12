import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    LogisticRegression,
)

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    RandomForestClassifier,
    GradientBoostingClassifier,
)


# ==========================================================
# TARGET SELECTION
# ==========================================================

def choose_target(df, requested=None):

    # 1. User explicitly specified target
    if requested and requested in df.columns:
        return requested

    columns = list(df.columns)

    # 2. Common prediction target names
    preferred_targets = [
        "target",
        "Target",
        "label",
        "Label",
        "y",
        "Y",
        "outcome",
        "Outcome",
        "response",
        "Response",
        "survived",
        "Survived",
        "price",
        "Price",
        "sales",
        "Sales",
        "temperature",
        "Temperature",
        "Temperature_C",
        "rainfall",
        "Rainfall_mm",
    ]

    for target in preferred_targets:
        if target in columns:
            return target

    # 3. Remove ID / identifier columns
    excluded = []

    for col in columns:

        name = (
            str(col)
            .lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if (
            name.endswith("id")
            or name == "id"
            or "identifier" in name
        ):
            excluded.append(col)

    # 4. Select remaining numeric columns
    numeric = [
        col
        for col in df.select_dtypes(
            include=np.number
        ).columns
        if col not in excluded
    ]

    if numeric:
        return numeric[0]

    # 5. If no numeric target exists,
    # use last non-ID column
    candidates = [
        col
        for col in columns
        if col not in excluded
    ]

    if candidates:
        return candidates[-1]

    return None


# ==========================================================
# DATETIME FEATURE ENGINEERING
# ==========================================================

def prepare_features(X):

    X = X.copy()

    datetime_columns = X.select_dtypes(
        include=["datetime64[ns]", "datetime64[ns, UTC]"]
    ).columns.tolist()

    for c in datetime_columns:

        X[c + "_year"] = X[c].dt.year
        X[c + "_month"] = X[c].dt.month
        X[c + "_day"] = X[c].dt.day
        X[c + "_dayofyear"] = X[c].dt.dayofyear
        X[c + "_dayofweek"] = X[c].dt.dayofweek

        X.drop(
            columns=[c],
            inplace=True
        )

    return X


# ==========================================================
# PREPROCESSOR
# ==========================================================

def build_preprocessor(X):

    numeric = X.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical = X.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    transformers = []

    if numeric:

        transformers.append(
            (
                "num",
                Pipeline(
                    [
                        (
                            "imputer",
                            SimpleImputer(
                                strategy="median"
                            ),
                        ),
                        (
                            "scaler",
                            StandardScaler()
                        ),
                    ]
                ),
                numeric,
            )
        )

    if categorical:

        transformers.append(
            (
                "cat",
                Pipeline(
                    [
                        (
                            "imputer",
                            SimpleImputer(
                                strategy="most_frequent"
                            ),
                        ),
                        (
                            "onehot",
                            OneHotEncoder(
                                handle_unknown="ignore"
                            ),
                        ),
                    ]
                ),
                categorical,
            )
        )

    return ColumnTransformer(
        transformers=transformers
    )


# ==========================================================
# AUTOMATIC PROBLEM TYPE DETECTION
# ==========================================================

def detect_problem_type(y):

    # Non-numeric target = classification
    if not pd.api.types.is_numeric_dtype(y):
        return "classification"

    unique_values = y.nunique()

    # Binary / small number of unique values
    if unique_values <= 10:

        # Integer-like small categorical target
        if (
            pd.api.types.is_integer_dtype(y)
            or unique_values <= 2
        ):
            return "classification"

    return "regression"


# ==========================================================
# REGRESSION MODELS
# ==========================================================

def regression_models(df, target):

    data = df.copy()

    data = data.dropna(
        subset=[target]
    )

    if len(data) < 30:

        return {
            "status": "INSUFFICIENT_DATA",
            "message": "Fewer than 30 usable rows.",
        }

    X = data.drop(
        columns=[target]
    )

    y = data[target]

    X = prepare_features(X)

    preprocessor = build_preprocessor(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    models = {

        "Linear Regression":
            LinearRegression(),

        "Ridge":
            Ridge(alpha=1.0),

        "Random Forest":
            RandomForestRegressor(
                n_estimators=200,
                random_state=42,
                n_jobs=-1,
            ),

        "Gradient Boosting":
            GradientBoostingRegressor(
                random_state=42
            ),
    }

    results = {}

    best_name = None
    best_rmse = float("inf")

    for name, model in models.items():

        pipe = Pipeline(
            [
                (
                    "preprocess",
                    preprocessor
                ),
                (
                    "model",
                    model
                ),
            ]
        )

        pipe.fit(
            X_train,
            y_train
        )

        pred = pipe.predict(
            X_test
        )

        mae = mean_absolute_error(
            y_test,
            pred
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                pred
            )
        )

        r2 = r2_score(
            y_test,
            pred
        )

        results[name] = {

            "MAE": round(
                float(mae),
                4
            ),

            "RMSE": round(
                float(rmse),
                4
            ),

            "R2": round(
                float(r2),
                4
            ),
        }

        if rmse < best_rmse:

            best_rmse = rmse
            best_name = name

    return {

        "status": "OK",

        "problem_type":
            "regression",

        "target":
            target,

        "rows_used":
            len(data),

        "test_size":
            len(y_test),

        "models":
            results,

        "best_model":
            best_name,

        "selection_metric":
            "RMSE (lower is better)",
    }


# ==========================================================
# CLASSIFICATION MODELS
# ==========================================================

def classification_models(df, target):

    data = df.copy()

    data = data.dropna(
        subset=[target]
    )

    if len(data) < 30:

        return {
            "status": "INSUFFICIENT_DATA",
            "message": "Fewer than 30 usable rows.",
        }

    X = data.drop(
        columns=[target]
    )

    y = data[target]

    # Classification requires at least 2 classes
    if y.nunique() < 2:

        return {
            "status": "INVALID_TARGET",
            "message":
                "The target contains fewer than two classes.",
        }

    X = prepare_features(X)

    preprocessor = build_preprocessor(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    models = {

        "Logistic Regression":
            LogisticRegression(
                max_iter=1000
            ),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=200,
                random_state=42,
                n_jobs=-1,
            ),

        "Gradient Boosting":
            GradientBoostingClassifier(
                random_state=42
            ),
    }

    results = {}

    best_name = None
    best_f1 = -1

    for name, model in models.items():

        pipe = Pipeline(
            [
                (
                    "preprocess",
                    preprocessor
                ),
                (
                    "model",
                    model
                ),
            ]
        )

        pipe.fit(
            X_train,
            y_train
        )

        pred = pipe.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            pred
        )

        precision = precision_score(
            y_test,
            pred,
            average="weighted",
            zero_division=0,
        )

        recall = recall_score(
            y_test,
            pred,
            average="weighted",
            zero_division=0,
        )

        f1 = f1_score(
            y_test,
            pred,
            average="weighted",
            zero_division=0,
        )

        results[name] = {

            "Accuracy": round(
                float(accuracy),
                4
            ),

            "Precision": round(
                float(precision),
                4
            ),

            "Recall": round(
                float(recall),
                4
            ),

            "F1": round(
                float(f1),
                4
            ),
        }

        if f1 > best_f1:

            best_f1 = f1
            best_name = name

    return {

        "status": "OK",

        "problem_type":
            "classification",

        "target":
            target,

        "rows_used":
            len(data),

        "test_size":
            len(y_test),

        "classes":
            int(y.nunique()),

        "models":
            results,

        "best_model":
            best_name,

        "selection_metric":
            "Weighted F1 (higher is better)",
    }


# ==========================================================
# MAIN ML FUNCTION
# ==========================================================

def run_ml_analysis(df, target=None):

    selected_target = choose_target(
        df,
        target
    )

    if selected_target is None:

        return {
            "status": "NO_TARGET",
            "message":
                "No suitable prediction target could be identified.",
        }

    y = df[selected_target]

    problem_type = detect_problem_type(
        y
    )

    if problem_type == "classification":

        return classification_models(
            df,
            selected_target
        )

    return regression_models(
        df,
        selected_target
    )
