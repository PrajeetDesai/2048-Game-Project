import argparse
import json

import nltk
import pandas as pd

from src.analysis import fairness_analysis, shap_top_tokens, temporal_trend
from src.config import GROUP_COLUMN, LABEL_COLUMN, TEXT_COLUMN
from src.modeling import evaluate_model, load_baseline, prepare_features, train_baseline
from src.preprocess import preprocess_frame, split_dataset
from src.transformer_pipeline import fine_tune_transformer


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True, help="Path to labeled csv with text,label columns")
    p.add_argument("--baseline", choices=["logreg", "svm"], default="logreg")
    p.add_argument("--train-transformer", action="store_true")
    p.add_argument("--output", default="mental_health_risk_app/artifacts/metrics.json")
    return p.parse_args()


def main():
    args = parse_args()
    nltk.download("vader_lexicon", quiet=True)

    df = pd.read_csv(args.data)
    df = preprocess_frame(df)
    bundle = split_dataset(df)

    model, vectorizer = train_baseline(bundle.train, args.baseline)
    metrics = evaluate_model(model, vectorizer, bundle.test)

    x_test = prepare_features(bundle.test, vectorizer, fit=False)
    y_pred = model.predict(x_test)
    fairness = fairness_analysis(bundle.test[LABEL_COLUMN].values, y_pred, bundle.test[GROUP_COLUMN])
    shap_terms = shap_top_tokens(model, vectorizer, bundle.test)

    if hasattr(model, "predict_proba"):
        risk_scores = model.predict_proba(x_test)
        risk_series = risk_scores[:, 1] if risk_scores.shape[1] == 2 else risk_scores.max(axis=1)
    else:
        decision = model.decision_function(x_test)
        risk_series = 1 / (1 + pow(2.71828, -decision))

    temporal = temporal_trend(bundle.test, risk_series)

    output = {
        "baseline_metrics": metrics,
        "fairness": fairness,
        "top_shap_terms": shap_terms,
        "temporal_preview": temporal.head(20).to_dict(orient="records"),
        "ethics_disclaimer": "Not a diagnostic tool. Use only for supportive triage and human review.",
    }

    if args.train_transformer:
        labels = sorted(df[LABEL_COLUMN].unique().tolist())
        label2id = {k: i for i, k in enumerate(labels)}
        fine_tune_transformer(bundle.train.copy(), bundle.val.copy(), label2id)
        output["transformer"] = "fine_tuned"

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"Training complete. Metrics saved to {args.output}")


if __name__ == "__main__":
    main()
