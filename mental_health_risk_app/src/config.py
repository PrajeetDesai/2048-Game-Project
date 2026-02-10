from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = BASE_DIR / "artifacts"
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

BASELINE_MODEL_PATH = ARTIFACT_DIR / "baseline_model.joblib"
VECTORIZER_PATH = ARTIFACT_DIR / "tfidf_vectorizer.joblib"
TRANSFORMER_DIR = ARTIFACT_DIR / "transformer_model"
REFERENCE_STATS_PATH = ARTIFACT_DIR / "reference_stats.json"
PREDICTION_LOG_PATH = LOG_DIR / "prediction_log.csv"

TEXT_COLUMN = "text"
LABEL_COLUMN = "label"
USER_ID_COLUMN = "user_id"
TIMESTAMP_COLUMN = "timestamp"
GROUP_COLUMN = "group"
