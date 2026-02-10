import re
import string
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split

from .config import (
    GROUP_COLUMN,
    LABEL_COLUMN,
    TEXT_COLUMN,
    TIMESTAMP_COLUMN,
    USER_ID_COLUMN,
)

URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
MENTION_PATTERN = re.compile(r"@\w+")
WHITESPACE_PATTERN = re.compile(r"\s+")


@dataclass
class DatasetBundle:
    train: pd.DataFrame
    val: pd.DataFrame
    test: pd.DataFrame


def clean_text(text: str) -> str:
    text = text.lower()
    text = URL_PATTERN.sub(" ", text)
    text = MENTION_PATTERN.sub(" ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = WHITESPACE_PATTERN.sub(" ", text).strip()
    return text


def add_sentiment_features(df: pd.DataFrame) -> pd.DataFrame:
    sia = SentimentIntensityAnalyzer()
    sentiments = df[TEXT_COLUMN].fillna("").apply(sia.polarity_scores)
    df = df.copy()
    for col in ["neg", "neu", "pos", "compound"]:
        df[f"sent_{col}"] = sentiments.apply(lambda x: x[col])
    return df


def add_emotion_proxy_features(df: pd.DataFrame) -> pd.DataFrame:
    """Simple lexicon proxies; replace with richer emotion model if available."""
    emotion_lexicon = {
        "sadness": {"sad", "empty", "hopeless", "down", "tired", "alone"},
        "anxiety": {"anxious", "panic", "worry", "nervous", "stress", "overwhelmed"},
        "anger": {"angry", "furious", "irritated", "hate"},
        "joy": {"happy", "grateful", "hopeful", "calm", "better"},
    }
    df = df.copy()
    tokens = df[TEXT_COLUMN].fillna("").str.split()
    for emotion, words in emotion_lexicon.items():
        df[f"emo_{emotion}"] = tokens.apply(lambda tok: sum(1 for t in tok if t in words))
    return df


def preprocess_frame(df: pd.DataFrame) -> pd.DataFrame:
    if TEXT_COLUMN not in df.columns or LABEL_COLUMN not in df.columns:
        raise ValueError(f"Input data must include '{TEXT_COLUMN}' and '{LABEL_COLUMN}' columns")

    df = df.copy()
    df[TEXT_COLUMN] = df[TEXT_COLUMN].fillna("").apply(clean_text)
    if TIMESTAMP_COLUMN in df.columns:
        df[TIMESTAMP_COLUMN] = pd.to_datetime(df[TIMESTAMP_COLUMN], errors="coerce")
    if USER_ID_COLUMN not in df.columns:
        df[USER_ID_COLUMN] = "anonymous"
    if GROUP_COLUMN not in df.columns:
        df[GROUP_COLUMN] = "unknown"

    df = add_sentiment_features(df)
    df = add_emotion_proxy_features(df)
    return df


def split_dataset(
    df: pd.DataFrame,
    test_size: float = 0.15,
    val_size: float = 0.15,
    random_state: int = 42,
    stratify: bool = True,
) -> DatasetBundle:
    strat = df[LABEL_COLUMN] if stratify else None
    train_val, test = train_test_split(
        df, test_size=test_size, random_state=random_state, stratify=strat
    )
    strat_tv = train_val[LABEL_COLUMN] if stratify else None
    val_ratio = val_size / (1 - test_size)
    train, val = train_test_split(
        train_val, test_size=val_ratio, random_state=random_state, stratify=strat_tv
    )
    return DatasetBundle(train=train.reset_index(drop=True), val=val.reset_index(drop=True), test=test.reset_index(drop=True))


def handle_class_imbalance(labels: pd.Series) -> dict:
    counts = labels.value_counts().to_dict()
    total = len(labels)
    num_classes = len(counts)
    return {klass: total / (num_classes * count) for klass, count in counts.items()}
