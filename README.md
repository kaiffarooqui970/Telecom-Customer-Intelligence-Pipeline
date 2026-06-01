# 📊 Telecom Customer Intelligence Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Playwright](https://img.shields.io/badge/Playwright-Async-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)

An end-to-end data engineering and analytics pipeline that merges historical telecommunications churn records with live, web-scraped sentiment to predict and understand customer flight risk.

## 🎯 The Business Problem
Traditional churn models are inherently **reactive**—they rely on historical billing data to identify trends only *after* a customer has decided to leave. To proactively reduce churn, businesses need real-time context. 

This project bridges that gap by enriching static, tabular CRM data with **live Natural Language Processing (NLP) sentiment scoring** extracted directly from public customer reviews.

## 🏗️ Architecture & Data Flow
This project moves beyond a standard Jupyter Notebook to demonstrate a complete Extract, Transform, Load (ETL) and visualization architecture:

1. **Extraction (Web Scraping):** An asynchronous Playwright engine navigates dynamic, JavaScript-heavy review platforms (e.g., Trustpilot) to extract live customer feedback, bypassing basic bot protections and handling pagination.
2. **Transformation (NLP & Pandas):** Unstructured text data is cleaned and passed through a TextBlob NLP model to calculate polarity and assign quantifiable sentiment categories (Positive, Neutral, Negative).
3. **Loading (Relational Database):** Transformed data is loaded into a local SQLite database, establishing a structured relationship between historical churn metrics and real-time sentiment.
4. **Visualization (Streamlit):** A live front-end application connects to the SQLite database and base CSVs to visualize churn drivers, customer lifetime value (CLV), and sentiment spikes.

## 🛠️ Technical Stack
* **Data Engineering & ETL:** `pandas`, `sqlite3`
* **Web Scraping & Automation:** `playwright` (Async API)
* **Machine Learning / NLP:** `textblob`
* **Frontend Dashboard:** `streamlit`

## 🚀 Quick Start / Local Deployment

To run this pipeline locally on your machine:

**1. Clone the repository**
```bash
git clone [https://github.com/kaiffarooqui970/Telecom-Customer-Intelligence-Pipeline.git](https://github.com/kaiffarooqui970/Telecom-Customer-Intelligence-Pipeline.git)
cd Telecom-Customer-Intelligence-Pipeline
2. Set up the virtual environment

Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
3. Execute the ETL Pipeline

Bash
# Scrape live data and build the SQLite database
python scripts/build_database.py
4. Launch the Intelligence Dashboard

Bash
streamlit run app/dashboard.py
Developed as part of an MSc Data Science portfolio at Lancaster University Leipzig.


***

### Why this works:
1. **The Shields (Badges):** It immediately visually communicates your tech stack at the very top.
2. **The Architecture Section:** It proves you understand the full ETL lifecycle (Extract, Transform, Load), which is exactly what senior data engineers look for.
3. **The Clean Formatting:** It uses bolding and lists to make it highly scannable for a recruiter who is reviewing 50 resumes a day.

Once you commit and push this `README.md` to your main branch, your GitHub repository will look incredibly professional. 

Are you ready to deploy the dashboard live to the Streamlit Community Cloud so you can put a working URL directly on your resume?
