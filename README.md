# 📈 Stock Sentiment Analysis Web App

A full-stack, responsive web application that performs real-time stock sentiment analysis using live data from Reddit and global news sources. Sentiment classification is performed using FinBERT (a financial-domain BERT model), and results are visualized with interactive pie and bar charts.

## 🚀 Features

- 🔍 Real-time sentiment analysis of any stock symbol
- 📰 Fetches data from Reddit (via PRAW) and online news (via NewsAPI)
- 🤖 Uses FinBERT NLP model for financial sentiment classification
- 📊 Displays sentiment distribution (positive/neutral/negative) using Pie Charts
- 📈 Shows sentiment trend over time via stacked Bar Charts
- 🖥️ Built with a clean, responsive, and interactive frontend using React
- 🔗 Backend built with Flask, providing RESTful APIs


# 📁 Project Structure
├── Server
│   ├── app.py
│   ├── utils/
│   ├── models/
│   └── ...
├── Client
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── App.css
│   └── ...
