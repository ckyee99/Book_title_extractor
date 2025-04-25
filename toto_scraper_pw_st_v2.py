import streamlit as st
import pandas as pd
from io import StringIO
from playwright.sync_api import sync_playwright

st.set_page_config(page_title="TOTO Draw Scraper", layout="wide")

# --- Playwright scraper function ---
def scrape_toto_results():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx")
        page.wait_for_timeout(6000)

        blocks = page.locator(".drawresult")
        count = blocks.count()

        results = []

        for i in range(count):
            block = blocks.nth(i)

            header = block.locator(".drawresultheader").text_content().strip()
            draw_date = header.split("TOTO Draw")[0].strip()

            numbers = block.locator(".drawnumber span")
            if numbers.count() < 7:
                continue  # skip incomplete results

            win_nums = [numbers.nth(j).text_content() for j in range(numbers.count() - 1)]
            add_num = numbers.nth(numbers.count() - 1).text_content()

            group1_winners = "Unknown"
            try:
                rows = block.locator("table tr")
                for r in range(rows.count()):
                    row = rows.nth(r)
                    if "Group 1" in row.text_content():
                        group1_winners = row.locator("td").nth(2).text_content().strip()
                        break
            except:
                pass

            results.append({
                "Draw Number": count - i,
                "Date": draw_date,
                "Winning Numbers": ", ".join(win_nums),
                "Additional Number": add_num,
                "Group 1 Winners": group1_winners
            })

        browser.close()
        return pd.DataFrame(results)

# --- Streamlit UI ---
st.title("🎲 Singapore Pools TOTO Draw Scraper")

if st.button("🔄 Fetch Latest Draw Results"):
    with st.spinner("Scraping TOTO results..."):
        df = scrape_toto_results()
        if df.empty or "Draw Number" not in df.columns:
            st.error("❌ No draw data was found. Please check the site or try again.")
            st.stop()
        st.session_state["toto_df"] = df
        st.success(f"✅ Fetched {len(df)} draws!")

if "toto_df" in st.session_state:
    df = st.session_state["toto_df"]
    if "Draw Number" not in df.columns:
        st.error("❌ The required data column 'Draw Number' is missing.")
        st.stop()

    draw_nums = df["Draw Number"].tolist()

    st.subheader("🎯 View Single or Multiple Draws")
    draw_mode = st.radio("Select mode", ["Single", "Multiple", "Range"])

    if draw_mode == "Single":
        selected = st.selectbox("Choose a draw number:", draw_nums)
        st.dataframe(df[df["Draw Number"] == selected])

    elif draw_mode == "Multiple":
        selected = st.multiselect("Choose draw numbers:", draw_nums)
        st.dataframe(df[df["Draw Number"].isin(selected)])

    elif draw_mode == "Range":
        min_draw = min(draw_nums)
        max_draw = max(draw_nums)
        draw_range = st.slider("Select draw number range", min_draw, max_draw, (max_draw-10, max_draw))
        selected_df = df[(df["Draw Number"] >= draw_range[0]) & (df["Draw Number"] <= draw_range[1])]
        st.dataframe(selected_df)

    st.download_button(
        label="📥 Download All Draws as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="toto_draws.csv",
        mime="text/csv"
    )
