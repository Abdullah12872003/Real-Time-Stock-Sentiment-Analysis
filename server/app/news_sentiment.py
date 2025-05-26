# news_sentiment.py
import requests
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch

# Initialize FinBERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = softmax(outputs.logits, dim=1)
        sentiment_id = torch.argmax(probs).item()
        sentiment_label = ['neutral', 'positive', 'negative'][sentiment_id]  # lowercased
        return sentiment_label

def fetch_news_and_analyze(stock_name, api_key):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': stock_name,
        'language': 'en',
        'pageSize': 100,
        'apiKey': api_key
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise ValueError('NewsAPI request failed')

    articles = response.json().get('articles', [])
    df = pd.DataFrame(articles)[['title', 'description', 'publishedAt']]
    df.dropna(subset=['description'], inplace=True)
    df['text'] = df['title'] + ". " + df['description']
    df['sentiment'] = df['text'].apply(analyze_sentiment)
    df['date'] = pd.to_datetime(df['publishedAt']).dt.date

    # Ensure consistent order and lowercase keys
    sentiment_counts = df['sentiment'].value_counts().reindex(['positive', 'neutral', 'negative']).fillna(0).to_dict()

    trend_data = df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
    trend_data = trend_data.reindex(columns=['positive', 'neutral', 'negative'], fill_value=0)
    trend_data = trend_data.reset_index().to_dict(orient='records')

    return sentiment_counts, trend_data
