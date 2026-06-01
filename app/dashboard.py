import streamlit as st
import pandas as pd
import sqlite3
import os

# --- Configuration & Styling ---
st.set_page_config(page_title="Churn & Sentiment Intelligence", layout="wide")
st.title("📊 Customer Churn & Sentiment Intelligence")
st.markdown("Merging historical churn records with live scraped customer sentiment.")

# --- File Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "churn_analysis.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "telco_churn.csv")

# --- Data Loading Functions ---
@st.cache_data
def load_base_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        # Convert TotalCharges to numeric, coercing errors to NaN
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        return df
    return None

def load_sentiment_data():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM customer_reviews", conn)
        conn.close()
        return df
    return None

df_churn = load_base_data()
df_sentiment = load_sentiment_data()

# --- Dashboard Layout ---
if df_churn is not None and df_sentiment is not None:
    
    # 1. Top Level KPIs
    st.subheader("Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    churn_rate = (df_churn['Churn'] == 'Yes').mean() * 100
    avg_ltv = df_churn['TotalCharges'].mean()
    total_reviews = len(df_sentiment)
    negative_ratio = (len(df_sentiment[df_sentiment['sentiment_category'] == 'Negative']) / total_reviews) * 100 if total_reviews > 0 else 0

    col1.metric("Historical Churn Rate", f"{churn_rate:.1f}%")
    col2.metric("Avg Customer Lifetime Value", f"${avg_ltv:,.2f}")
    col3.metric("Live Scraped Reviews", total_reviews)
    col4.metric("Current Negative Sentiment", f"{negative_ratio:.1f}%")

    st.divider()

    # 2. Visualizations
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Historical Churn by Contract Type")
        # Grouping data for a bar chart
        contract_churn = df_churn.groupby(['Contract', 'Churn']).size().unstack()
        st.bar_chart(contract_churn)
        st.caption("Month-to-month contracts represent the highest flight risk.")

    with col_right:
        st.subheader("Live Customer Sentiment (NLP)")
        # Grouping sentiment data
        sentiment_counts = df_sentiment['sentiment_category'].value_counts()
        st.bar_chart(sentiment_counts, color="#ff4b4b")
        st.caption("Derived via TextBlob polarity scoring on recently scraped web reviews.")

    st.divider()

    # 3. Raw Data Explorer (For Recruiters)
    st.subheader("Data Inspector")
    tab1, tab2 = st.tabs(["Scraped NLP Database (SQLite)", "Historical Baseline (CSV)"])
    
    with tab1:
        st.dataframe(df_sentiment[['reviewer_name', 'sentiment_category', 'review_text']], use_container_width=True)
    with tab2:
        st.dataframe(df_churn.head(100), use_container_width=True)

else:
    st.error("⚠️ Data files missing. Please ensure the CSV and SQLite DB exist in the 'data' directory.")