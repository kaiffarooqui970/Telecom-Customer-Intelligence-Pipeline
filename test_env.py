import pandas as pd
import streamlit as ui
from playwright.sync_api import sync_playwright

print("Pandas version:", pd.__version__)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    print("Playwright Chromium launched successfully!")
    browser.close()

print("Environment is ready for development.")