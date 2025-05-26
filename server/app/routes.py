from flask import Blueprint, request, jsonify
from .reddit_client import fetch_reddit_data
from .sentiment import analyze_sentiment
from .news_sentiment import fetch_news_and_analyze  # Import the new function for news sentiment analysis

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return 'Welcome to the Sentiment Analysis API. Use the /analyze endpoint with a stock name.'

@bp.route('/analyze', methods=['GET'])
def analyze():
    stock = request.args.get('stock')
    try:
        df = fetch_reddit_data(stock)
        sentiment_counts, trend_data = analyze_sentiment(df)
        return jsonify({
            'sentiment_counts': sentiment_counts,
            'trend_data': trend_data
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/news-analyze', methods=['GET'])
def news_analyze():
    stock = request.args.get('stock')
    api_key = 'fc175677d2554994a97f73b4d748ce6b'  # Replace with your NewsAPI key
    try:
        sentiment_counts, trend_data = fetch_news_and_analyze(stock, api_key)  # Call the function from news_sentiment.py
        return jsonify({
            'sentiment_counts': sentiment_counts,
            'trend_data': trend_data
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500