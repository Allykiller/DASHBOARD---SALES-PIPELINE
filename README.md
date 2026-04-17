Sales Pipeline Analysis Dashboard
Overview

This project analyzes a sales pipeline to identify bottlenecks, improve conversion rates, and generate actionable business insights.
It combines data analysis and visualization to support decision-making in sales strategy.

Objective

The goal of this project is to:

Understand the performance of the sales funnel
Identify drop-off points in the pipeline
Analyze conversion efficiency
Provide insights to improve revenue generation
🛠️ Tools & Technologies
Python (Pandas)
Data visualization libraries
Analytical dashboard
Structured dataset

Dashboard Preview

Key Metrics
Total Deals: 8,800
Revenue: R$ 10.01M
Conversion Rate: 63.2%
Average Ticket: R$ 2,361
Sales Cycle: 52 days

Key Insights
Approximately 48% of deals are successfully converted, indicating solid overall performance
Around 28% of deals are lost, suggesting inefficiencies in qualification or negotiation stages
Nearly 18% of opportunities remain open, indicating possible delays in pipeline progression
The presence of null values (~5%) highlights data quality issues, which may impact decision-making

Analysis Performed
Funnel distribution (Won, Lost, Open)
Conversion rate evaluation
Revenue analysis
Sales performance overview

How to Run
pip install -r requirements.txt
python dashboard.py

Project Structure
project/
├── dashboard.py
├── analysis.py
├── data/
│   └── dataset files
├── requirements.txt
└── README.md

Future Improvements
Deploy as an interactive web app (Streamlit)
Automate data ingestion (ETL pipeline)
Add filtering by region, sales rep, and lead source
Improve data modeling and scalability

Business Impact

This project helps identify inefficiencies in the sales funnel and supports strategic decisions to improve conversion rates, optimize the sales process, and increase revenue performance.
