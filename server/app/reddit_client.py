import praw
import re
import pandas as pd
from datetime import datetime

reddit = praw.Reddit(client_id='Azfpp9YrmleMo9RYpn1mNA',
                     client_secret='V15kph1vxGjilgSaaOU4hWhGrpU0pg',
                     user_agent='Scrapper/for/Senti',
                     check_for_async=False)

def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def fetch_reddit_data(stock):
    subreddit_name = "IndianStockMarket"
    search_query = stock

    metadata = []
    texts_to_analyze = []

    for submission in reddit.subreddit(subreddit_name).search(search_query, sort='hot', limit=100):
        try:
            submission.comment_sort = "best"
            submission.comment_limit = 3
            submission.comments.replace_more(limit=0)
            comments = submission.comments.list()
            comments = comments[1:] if len(comments) > 1 else []

            post_text = f"{submission.title} {submission.selftext}"
            comment_texts = " ".join([comment.body for comment in comments])
            full_text = clean_text(f"{post_text} {comment_texts}")

            if len(full_text) < 20:
                continue

            metadata.append({
                "post_title": submission.title,
                "post_body": submission.selftext,
                "combined_comments": comment_texts,
                "created_utc": datetime.utcfromtimestamp(submission.created_utc)
            })
            texts_to_analyze.append(full_text)
        except Exception as e:
            print(f"Skipped post due to error: {e}")
            continue

    df = pd.DataFrame(metadata)
    df['full_text'] = texts_to_analyze
    return df
