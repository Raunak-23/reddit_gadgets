# install once: pip install transformers torch --upgrade
from transformers import pipeline
import torch, re, pandas as pd, os

class ABSAWrapper:
    def __init__(self, model_name="yangheng/deberta-v3-base-absa-v1.1"):
        self.pipe = pipeline(
            "text-classification",
            model=model_name,
            tokenizer=model_name,
            truncation=True,
            device=0 if torch.cuda.is_available() else -1,
            top_k=None  # we want all labels
        )

    def predict(self, text):
        """
        Returns list of dicts: [{'label': 'Positive', 'score': 0.97}, ...]
        Only keep aspects with confidence > 0.5
        """
        try:
            preds = self.pipe(text[:512])
            return [p for p in preds if p["score"] > 0.5]
        except Exception:
            return []

absa = ABSAWrapper()