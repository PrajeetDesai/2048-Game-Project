import json
from typing import Dict, List

import numpy as np
import pandas as pd
import shap
from sklearn.metrics import recall_score

from .config import GROUP_COLUMN, LABEL_COLUMN, REFERENCE_STATS_PATH, TEXT_COLUMN, USER_ID_COLUMN, TIMESTAMP_COLUMN
from .modeling import AUX_FEATURES, prepare_features


def shap_top_tokens(model, vectorizer, df: pd.DataFrame, sample_size: int = 50) -> Dict[str, List[float]]:
    sample = df.head(sample_size)
    x_sample = prepare_features(sample, vectorizer, fit=False)
    explainer = shap.LinearExplainer(model, x_sample, feature_perturbation="interventional")
    values = explainer.shap_values(x_sample)
    token_names = vectorizer.get_feature_names_out().tolist() + AUX_FEATURES
    mean_abs = np.abs(values).mean(axis=0)
    top_idx = np.argsort(mean_abs)[-20:][::-1]
    return {token_names[i]: float(mean_abs[i]) for i in top_idx}


def fairness_analysis(y_true: np.ndarray, y_pred: np.ndarray, groups: pd.Series) -> Dict[str, Dict[str, float]]:
    frame = pd.DataFrame({"y_true": y_true, "y_pred": y_pred, "group": groups})
    output = {}
    for grp, sub in frame.groupby("group"):
        output[str(grp)] = {
            "recall": float(recall_score(sub["y_true"], sub["y_pred"], average="weighted", zero_division=0)),
            "sample_size": int(len(sub)),
        }
    recalls = [v["recall"] for v in output.values()]
    if recalls:
        output["summary"] = {"recall_gap": float(max(recalls) - min(recalls))}
    return output


def temporal_trend(df: pd.DataFrame, prediction_scores: np.ndarray) -> pd.DataFrame:
    if TIMESTAMP_COLUMN not in df.columns:
        return pd.DataFrame()
    frame = df[[USER_ID_COLUMN, TIMESTAMP_COLUMN]].copy()
    frame["risk_score"] = prediction_scores
    frame = frame.dropna(subset=[TIMESTAMP_COLUMN]).sort_values([USER_ID_COLUMN, TIMESTAMP_COLUMN])
    frame["rolling_risk"] = frame.groupby(USER_ID_COLUMN)["risk_score"].transform(lambda s: s.ewm(span=3).mean())
    frame["risk_delta"] = frame.groupby(USER_ID_COLUMN)["rolling_risk"].diff().fillna(0)
    return frame


def psi_score(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    quantiles = np.linspace(0, 1, bins + 1)
    breakpoints = np.quantile(expected, quantiles)
    expected_hist = np.histogram(expected, bins=breakpoints)[0] / len(expected)
    actual_hist = np.histogram(actual, bins=breakpoints)[0] / max(1, len(actual))
    expected_hist = np.where(expected_hist == 0, 1e-6, expected_hist)
    actual_hist = np.where(actual_hist == 0, 1e-6, actual_hist)
    return float(np.sum((actual_hist - expected_hist) * np.log(actual_hist / expected_hist)))


def monitor_drift(current_non_zero_mean: float) -> Dict[str, float]:
    if not REFERENCE_STATS_PATH.exists():
        return {"psi_proxy": 0.0, "alert": 0}
    stats = json.loads(REFERENCE_STATS_PATH.read_text())
    reference_value = stats["tfidf_non_zero_mean"]
    arr_ref = np.repeat(reference_value, 30)
    arr_cur = np.repeat(current_non_zero_mean, 30)
    psi = psi_score(arr_ref, arr_cur)
    return {"psi_proxy": psi, "alert": int(psi > 0.25)}
