import torch
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def batch_analyze_sentiment(texts):
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    sentiments = []
    for prob in probs:
        pos, neg, neu = prob[1], prob[2], prob[0]
        if pos > 0.55:
            sentiment = "positive"
        elif neg > 0.55:
            sentiment = "negative"
        elif neu > 0.95:
            sentiment = "neutral"
        else:
            sentiment = "positive" if pos > neg else "negative"
        sentiments.append(sentiment)
    return sentiments

def analyze_sentiment(df):
    df['sentiment'] = batch_analyze_sentiment(df['full_text'].tolist())
    df['created_utc'] = pd.to_datetime(df['created_utc'])
    df['date'] = df['created_utc'].dt.date

    sentiment_counts = df['sentiment'].value_counts().reindex(['positive', 'neutral', 'negative']).fillna(0).to_dict()
    trend_data = df.groupby(['date', 'sentiment']).size().unstack().fillna(0)
    trend_data = trend_data.replace([np.inf, -np.inf], 0).fillna(0).astype(int)
    trend_data = trend_data.reset_index().to_dict(orient='records')

    return sentiment_counts, trend_data
