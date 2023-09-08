import React, { useState, useEffect, PureComponent } from "react";
import { PieChart, Pie, Legend, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';
import { api } from "../utilities";



export default function HomePage() {


  const pieData = [
    { name: 'Net Worth', value: 120000 },
    { name: 'Debt', value: 12000 },
   
  ];

  const barExpenseData = [
    {
      name: '3 months ago',
      expenses: 1200,
    },
    {
      name: '2 months ago',
      expenses: 1398,
    },
    {
      name: 'last month',
      expenses: 1500,
    },
  ];
  

  
  return (
    <>
  <div className="main-page-contents">

    <button>pair your bank with plaid</button>
        <PieChart width={400} height={400}>
          <Pie
            dataKey="value"
            isAnimationActive={false}
            data={pieData}
            cx="50%"
            cy="50%"
            outerRadius={80}
            fill="#8884d8"
            label
          />
          <Tooltip />
        </PieChart>

        <BarChart
          width={500}
          height={300}
          data={barExpenseData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
          barSize={20}
        >
          <XAxis dataKey="name" scale="point" padding={{ left: 10, right: 10 }} />
          <YAxis />
          <Tooltip />
          <Legend />
          <CartesianGrid strokeDasharray="3 3" />
          <Bar dataKey="expenses" fill="#8884d8" background={{ fill: '#eee' }} />
        </BarChart>

        <div className="bank-info">
          <h3>Bank Information</h3>
          <ul>
            <li>Bank Balance: $XX,XXX</li>
            <li>Bank Transactions: XX</li>
          </ul>
        </div>
    
  </div>
  </>
  
);
}



