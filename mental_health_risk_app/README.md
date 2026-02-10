# Mental Health Risk Prediction (Local, End-to-End)

This module adds an end-to-end NLP workflow for estimating depression/stress risk from user text.

## What is included
- Dataset ingestion and preprocessing (cleaning, tokenization, sentiment, emotion proxy features).
- Class imbalance handling through class-weighted training.
- Baseline models: TF-IDF + Logistic Regression / Linear SVM.
- Transformer fine-tuning pipeline (DistilBERT; can be swapped to BERT/RoBERTa).
- Evaluation: Precision, Recall, F1, ROC-AUC, confusion matrix.
- Interpretability: SHAP top tokens for baseline, attention-token highlights for transformer.
- Fairness check: subgroup recall gap.
- Temporal modeling: exponential moving trend per user.
- Streamlit local app with confidence score, secure hash-based logging, and drift monitoring.

## Ethical safeguards
- This is **not** a medical diagnostic tool.
- Predictions are probabilistic triage signals and must be reviewed by qualified humans.
- Use local inference and hashed identifiers in logs to reduce privacy risk.

## Quick start
```bash
pip install -r mental_health_risk_app/requirements.txt
python mental_health_risk_app/train.py --data mental_health_risk_app/data/sample_mental_health.csv --baseline logreg
streamlit run mental_health_risk_app/app.py
```

## Data format
CSV columns expected:
- `text` (required)
- `label` (required; binary or multi-class)
- `user_id` (optional but recommended for temporal trend)
- `timestamp` (optional but recommended for temporal trend)
- `group` (optional subgroup for fairness analysis)
