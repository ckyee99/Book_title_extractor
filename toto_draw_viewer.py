import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from io import StringIO

# Placeholder URL - You need the actual data source or endpoint for real data
TOTO_ARCHIVE_URL = "https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx"

@st.cache_data(show_spinner=True)
def fetch_toto_draws():
    # This function should ideally scrape or request official TOTO draw results.
    # Since we can't access SP site programmatically due to protection, we simulate data.
    draws = []
    for i in range(1, 500):  # simulate 500 draws
        draws.append({
            "Draw Number": i,
            "Date": datetime(2023, 1, 1).strftime("%Y-%m-%d"),
            "Time": "18:30",
            "Winning Numbers": [1, 5, 9, 15, 23, 32],
            "Additional Number": 42,
            "Number of Winners": 3
        })
    return pd.DataFrame(draws)

# Title
st.title("🎲 Singapore Pools TOTO Draw Viewer")

# Fetch data
df = fetch_toto_draws()

df["Draw Number"] = df["Draw Number"].astype(int)
df.sort_values("Draw Number", ascending=False, inplace=True)

# Slider to scroll through draw numbers
selected_draw = st.slider("Scroll through Draw Numbers", int(df["Draw Number"].min()), int(df["Draw Number"].max()), int(df["Draw Number"].max()))
selected_df = df[df["Draw Number"] == selected_draw]

# Display selected draw
draw_info = selected_df.iloc[0]
st.subheader(f"Draw #{draw_info['Draw Number']} — {draw_info['Date']} at {draw_info['Time']}")
st.write(f"**Winning Numbers:** {draw_info['Winning Numbers']}")
st.write(f"**Additional Number:** {draw_info['Additional Number']}")
st.write(f"**Number of Winners:** {draw_info['Number of Winners']}")

# Export complete data to CSV
download_btn = st.download_button(
    label="📥 Download All TOTO Draws as CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name="toto_draws_up_to_2025-04-22.csv",
    mime="text/csv"
)

# Display full table below
st.markdown("---")
st.subheader("📋 Complete Draw Record")
st.dataframe(df, use_container_width=True, height=300)
