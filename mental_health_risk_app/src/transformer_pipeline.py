from typing import Dict

import numpy as np
import pandas as pd
from datasets import Dataset
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

from .config import LABEL_COLUMN, TEXT_COLUMN, TRANSFORMER_DIR


MODEL_NAME = "distilbert-base-uncased"


def _tokenize(tokenizer, batch):
    return tokenizer(batch[TEXT_COLUMN], truncation=True, padding="max_length", max_length=128)


def _metrics(eval_pred) -> Dict[str, float]:
    logits, labels = eval_pred
    probs = np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)
    preds = probs.argmax(axis=1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="weighted", zero_division=0)
    if probs.shape[1] == 2:
        roc_auc = roc_auc_score(labels, probs[:, 1])
    else:
        roc_auc = roc_auc_score(labels, probs, multi_class="ovr")
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
    }


def fine_tune_transformer(train_df: pd.DataFrame, val_df: pd.DataFrame, label2id: Dict[str, int]):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    num_labels = len(label2id)
    id2label = {v: k for k, v in label2id.items()}

    for df in [train_df, val_df]:
        df[LABEL_COLUMN] = df[LABEL_COLUMN].map(label2id)

    train_ds = Dataset.from_pandas(train_df[[TEXT_COLUMN, LABEL_COLUMN]])
    val_ds = Dataset.from_pandas(val_df[[TEXT_COLUMN, LABEL_COLUMN]])

    train_ds = train_ds.map(lambda x: _tokenize(tokenizer, x), batched=True)
    val_ds = val_ds.map(lambda x: _tokenize(tokenizer, x), batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=num_labels, label2id=label2id, id2label=id2label
    )

    args = TrainingArguments(
        output_dir=str(TRANSFORMER_DIR),
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=2,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        compute_metrics=_metrics,
    )
    trainer.train()
    trainer.save_model(str(TRANSFORMER_DIR))
    tokenizer.save_pretrained(str(TRANSFORMER_DIR))
