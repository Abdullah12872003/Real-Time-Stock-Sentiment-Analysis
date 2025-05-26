// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import InputForm from './components/InputForm';
import PieChartComponent from './components/PieChartComponent';
import BarChartComponent from './components/BarChartComponent';
import './App.css';

function App() {
  const [stock, setStock] = useState('');
  const [redditCounts, setRedditCounts] = useState(null);
  const [redditTrend, setRedditTrend] = useState(null);
  const [newsCounts, setNewsCounts] = useState(null);
  const [newsTrend, setNewsTrend] = useState(null);
  const [newsName, setNewsName] = useState('');
  const [redditName, setRedditName] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const newsRes = await axios.get(`http://localhost:5000/news-analyze?stock=${stock}`);
      setNewsCounts(newsRes.data.sentiment_counts);
      setNewsTrend(newsRes.data.trend_data);
      setNewsName(stock);

      const redditRes = await axios.get(`http://localhost:5000/analyze?stock=${stock}`);
      setRedditCounts(redditRes.data.sentiment_counts);
      setRedditTrend(redditRes.data.trend_data);
      setRedditName(stock);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="app-container">
      <div className="app-header">
      <h1>📈 Stock Sentiment Analyzer</h1>
        <p>Analyze stock sentiment from Reddit and News in real-time</p>
      </div>

      <div className="form-wrapper">
        <InputForm stock={stock} setStock={setStock} handleSubmit={handleSubmit} />
      </div>

      {newsCounts && newsTrend && (
        <>
          <div className="pie-charts">
            <div className="chart-card">
              <h2>News Sentiment of: {newsName}</h2>
              <PieChartComponent sentimentCounts={newsCounts} />
            </div>
            <div className="chart-card bar-chart-card">
              <h2>News Sentiment Trend</h2>
              <BarChartComponent trendData={newsTrend} />
            </div>
          </div>
        </>
      )}

      {redditCounts && redditTrend && (
        <>
          <div className="pie-charts">
            <div className="chart-card">
              <h2>Reddit Sentiment of: {redditName}</h2>
              <PieChartComponent sentimentCounts={redditCounts} />
            </div>
            <div className="chart-card bar-chart-card">
              <h2>Reddit Sentiment Trend</h2>
              <BarChartComponent trendData={redditTrend} />
            </div>
          </div>
        </> 
      )}
    </div>
  );
}

export default App;

