
// src/components/BarChartComponent.js
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = {
  positive: '#66bb6a',
  neutral: '#ffee58',
  negative: '#ef5350'
};

function BarChartComponent({ trendData }) {
  return (
    <div>
      <h2>Sentiment Trend Over Time</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={trendData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="positive" stackId="a" fill={COLORS.positive} />
          <Bar dataKey="neutral" stackId="a" fill={COLORS.neutral} />
          <Bar dataKey="negative" stackId="a" fill={COLORS.negative} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default BarChartComponent;
