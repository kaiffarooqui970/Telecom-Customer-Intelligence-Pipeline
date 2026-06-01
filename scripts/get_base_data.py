import pandas as pd
import os

# Define the path to save the dataset
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(DATA_DIR, "telco_churn.csv")

print("📥 Downloading IBM Telco Customer Churn dataset...")
url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"

# Read directly from the URL and save locally
df = pd.read_csv(url)
df.to_csv(CSV_PATH, index=False)

print(f"✅ Successfully downloaded {len(df)} rows to {CSV_PATH}")