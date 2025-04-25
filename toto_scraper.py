from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd


def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    return driver


def scrape_toto_results(max_draws=20):
    url = "https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx"
    driver = setup_driver()
    driver.get(url)

    time.sleep(5)  # Allow JavaScript to load content

    draw_blocks = driver.find_elements(By.CSS_SELECTOR, ".drawresult")

    results = []
    for block in draw_blocks[:max_draws]:
        try:
            header = block.find_element(By.CSS_SELECTOR, ".drawresultheader").text.strip()
            date = header.split("TOTO Draw")[0].strip()

            numbers = block.find_elements(By.CSS_SELECTOR, ".drawnumber span")
            win_nums = [n.text for n in numbers[:-1]]
            add_num = numbers[-1].text

            prize_table = block.find_element(By.CSS_SELECTOR, ".table-responsive table")
            rows = prize_table.find_elements(By.TAG_NAME, "tr")
            winners = None
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if cols and "Group 1" in cols[0].text:
                    winners = cols[2].text
                    break

            results.append({
                "Date": date,
                "Winning Numbers": win_nums,
                "Additional Number": add_num,
                "Number of Winners (Group 1)": winners
            })
        except Exception as e:
            print(f"Error parsing a draw block: {e}")
            continue

    driver.quit()
    return pd.DataFrame(results)


if __name__ == "__main__":
    df = scrape_toto_results(20)
    df.to_csv("toto_scraped_results.csv", index=False)
    print("✅ TOTO results saved to toto_scraped_results.csv")
