import hashlib
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from src.analysis import monitor_drift
from src.config import (
    BASELINE_MODEL_PATH,
    LABEL_COLUMN,
    LOG_DIR,
    PREDICTION_LOG_PATH,
    TEXT_COLUMN,
    TRANSFORMER_DIR,
    USER_ID_COLUMN,
)
from src.modeling import prepare_features
from src.preprocess import preprocess_frame

st.set_page_config(page_title="Mental Health Risk Estimator", layout="wide")
st.title("NLP-based Mental Health Risk Prediction (Local Inference)")
st.warning(
    "This tool is for educational triage support only and is NOT a medical diagnostic system. "
    "If someone may be in immediate danger, contact local emergency services or a licensed mental health professional."
)

model_choice = st.sidebar.selectbox("Model", ["Baseline TF-IDF", "Transformer"])
confidence_threshold = st.sidebar.slider("Risk alert threshold", 0.5, 0.95, 0.7, 0.01)

user_id = st.text_input("User ID (optional)", "anonymous")
text = st.text_area("Enter a journal entry or social post", height=220)


def secure_log(entry: dict):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    row = pd.DataFrame([entry])
    if PREDICTION_LOG_PATH.exists():
        row.to_csv(PREDICTION_LOG_PATH, mode="a", header=False, index=False)
    else:
        row.to_csv(PREDICTION_LOG_PATH, index=False)


if st.button("Predict risk"):
    if not text.strip():
        st.error("Please provide text.")
    else:
        frame = pd.DataFrame([{TEXT_COLUMN: text, LABEL_COLUMN: "unknown", USER_ID_COLUMN: user_id}])
        frame = preprocess_frame(frame)

        if model_choice == "Baseline TF-IDF":
            if not BASELINE_MODEL_PATH.exists():
                st.error("Baseline model artifacts not found. Run training script first.")
                st.stop()
            model = joblib.load(BASELINE_MODEL_PATH)
            vectorizer = joblib.load(BASELINE_MODEL_PATH.parent / "tfidf_vectorizer.joblib")
            features = prepare_features(frame, vectorizer, fit=False)
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(features)[0]
                score = float(np.max(probs))
                pred = model.classes_[int(np.argmax(probs))]
            else:
                decision = model.decision_function(features)
                score = float(1 / (1 + np.exp(-decision[0])))
                pred = model.predict(features)[0]
            drift = monitor_drift(float(features.getnnz(axis=1).mean()))
            attention_terms = "N/A for linear model"
        else:
            if not TRANSFORMER_DIR.exists():
                st.error("Transformer artifacts not found. Run fine-tuning first.")
                st.stop()
            tokenizer = AutoTokenizer.from_pretrained(str(TRANSFORMER_DIR))
            model = AutoModelForSequenceClassification.from_pretrained(str(TRANSFORMER_DIR), output_attentions=True)
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            output = model(**inputs)
            probs = output.logits.softmax(dim=-1).detach().numpy()[0]
            label_idx = int(np.argmax(probs))
            pred = model.config.id2label[label_idx]
            score = float(probs[label_idx])
            drift = {"psi_proxy": 0.0, "alert": 0}
            attention = output.attentions[-1].mean(dim=1).detach().numpy()[0]
            token_ids = inputs["input_ids"][0].tolist()
            tokens = tokenizer.convert_ids_to_tokens(token_ids)
            token_scores = attention[0]
            top_pairs = sorted(zip(tokens, token_scores), key=lambda x: x[1], reverse=True)[:8]
            attention_terms = ", ".join([f"{t}:{s:.2f}" for t, s in top_pairs])

        risk_flag = int(score >= confidence_threshold)
        st.subheader("Prediction")
        st.write(f"**Class:** {pred}")
        st.write(f"**Confidence:** {score:.3f}")
        st.write(f"**Risk alert:** {'Yes' if risk_flag else 'No'}")
        st.write(f"**Drift monitor PSI proxy:** {drift['psi_proxy']:.3f} ({'alert' if drift['alert'] else 'normal'})")
        st.write(f"**Influential terms / attention:** {attention_terms}")

        secure_log(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "user_hash": hashlib.sha256(user_id.encode()).hexdigest()[:12],
                "prediction": pred,
                "confidence": score,
                "risk_flag": risk_flag,
                "model": model_choice,
            }
        )
        st.success("Prediction logged locally with hashed user identifier.")
