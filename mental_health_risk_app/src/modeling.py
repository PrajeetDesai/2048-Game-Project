import json
from pathlib import Path
from typing import Dict, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.svm import LinearSVC
from sklearn.utils.class_weight import compute_class_weight
from scipy.sparse import csr_matrix, hstack

from .config import BASELINE_MODEL_PATH, LABEL_COLUMN, REFERENCE_STATS_PATH, TEXT_COLUMN, VECTORIZER_PATH

AUX_FEATURES = [
    "sent_neg",
    "sent_neu",
    "sent_pos",
    "sent_compound",
    "emo_sadness",
    "emo_anxiety",
    "emo_anger",
    "emo_joy",
]


def build_tfidf_vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95, max_features=30000)


def prepare_features(df: pd.DataFrame, vectorizer: TfidfVectorizer, fit: bool = False) -> csr_matrix:
    text = df[TEXT_COLUMN].fillna("")
    x_text = vectorizer.fit_transform(text) if fit else vectorizer.transform(text)
    aux = df.reindex(columns=AUX_FEATURES, fill_value=0.0).astype(float)
    x_aux = csr_matrix(aux.values)
    return hstack([x_text, x_aux])


def train_baseline(df_train: pd.DataFrame, model_type: str = "logreg"):
    vectorizer = build_tfidf_vectorizer()
    x_train = prepare_features(df_train, vectorizer, fit=True)
    y_train = df_train[LABEL_COLUMN].values

    classes = np.unique(y_train)
    weights = compute_class_weight(class_weight="balanced", classes=classes, y=y_train)
    class_weight = dict(zip(classes, weights))

    if model_type == "svm":
        model = LinearSVC(class_weight=class_weight)
    else:
        model = LogisticRegression(max_iter=300, class_weight=class_weight)

    model.fit(x_train, y_train)
    BASELINE_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, BASELINE_MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    reference_stats = {
        "tfidf_non_zero_mean": float(x_train.getnnz(axis=1).mean()),
        "aux_feature_mean": df_train.reindex(columns=AUX_FEATURES, fill_value=0.0).mean().to_dict(),
    }
    REFERENCE_STATS_PATH.write_text(json.dumps(reference_stats, indent=2))
    return model, vectorizer


def load_baseline() -> Tuple[object, TfidfVectorizer]:
    return joblib.load(BASELINE_MODEL_PATH), joblib.load(VECTORIZER_PATH)


def evaluate_model(model, vectorizer, df_eval: pd.DataFrame) -> Dict[str, object]:
    x_eval = prepare_features(df_eval, vectorizer, fit=False)
    y_true = df_eval[LABEL_COLUMN].values
    y_pred = model.predict(x_eval)

    if hasattr(model, "predict_proba"):
        y_scores = model.predict_proba(x_eval)
        roc_auc = roc_auc_score(y_true, y_scores[:, 1]) if y_scores.shape[1] == 2 else roc_auc_score(y_true, y_scores, multi_class="ovr")
    else:
        decision = model.decision_function(x_eval)
        roc_auc = roc_auc_score(y_true, decision)

    return {
        "precision": precision_score(y_true, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="weighted", zero_division=0),
        "f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        "roc_auc": roc_auc,
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "classification_report": classification_report(y_true, y_pred, zero_division=0),
    }
