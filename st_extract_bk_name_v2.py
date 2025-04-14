import streamlit as st
import os
import re

def extract_title(line: str) -> str:
    # Case 1: contains '--' or ' - [^-]+ - ' for typical patterns
    if '--' in line or re.search(r' - [^-]+ - ', line):
        title = re.split(r"--| - [^-]+ - ", line)[0].strip()
        print ("title 1:", title[0])
    else:
        # Case 2: author - title - extra
        # Split only on the FIRST ' - ', keep the rest intact
        parts = line.split(" - ", 1)
        title = parts[1].strip() if len(parts) > 1 else line.strip()
        print ("parts [0] :", parts[0])
        print ("title 2", title[0])

    return title

st.title("Book Title Extractor")

uploaded_file = st.file_uploader("Upload a .txt file with book lines", type=["txt"])
if uploaded_file:
    content = uploaded_file.read().decode("utf-8").splitlines()
    
    # Process each line individually
    titles = [extract_title(line) for line in content if line.strip()]

    st.subheader("Extracted Titles")
    for idx, title in enumerate(titles, 1):
        st.write(f"{idx}. {title}")

    # Prepare for download
    csv_ready = "\n".join([f"{idx}. {title}" for idx, title in enumerate(titles, 1)])
    st.download_button("Download Titles as .txt", csv_ready, "book_titles.txt")
