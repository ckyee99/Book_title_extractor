import streamlit as st
import os
import re
from pathlib import Path

def clean_filename(filename):
    # Remove 13-digit numbers (ISBNs)
    filename = re.sub(r'\b978\d{10}\b', '', filename)
    # Remove 32-character ASCII hex strings
    filename = re.sub(r'\b[a-fA-F0-9]{32}\b', '', filename)
    # Remove "Anna’s Archive" (both straight and curly apostrophes)
    filename = re.sub(r"Anna[’']s Archive", '', filename, flags=re.IGNORECASE)
    # Remove redundant separators
    filename = re.sub(r'\s*--\s*', ' -- ', filename)  # Normalize
    filename = re.sub(r'( -- ){2,}', ' -- ', filename)  # Remove extras
    return filename.strip().strip('-').strip()

def rename_files_in_directory(directory):
    renamed_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            old_path = os.path.join(root, file)
            if not os.path.isfile(old_path):
                continue
            new_name = clean_filename(Path(file).stem).strip() + Path(file).suffix
            new_path = os.path.join(root, new_name)
            if old_path != new_path:
                os.rename(old_path, new_path)
                renamed_files.append((file, new_name))
    return renamed_files

st.title("📚 Book Title Cleaner")

folder = st.text_input("Enter the path to the directory to scan (including subfolders):")

if st.button("Clean Book Titles"):
    if os.path.isdir(folder):
        renamed = rename_files_in_directory(folder)
        if renamed:
            st.success(f"Renamed {len(renamed)} files:")
            for old, new in renamed:
                st.write(f"✅ `{old}` → `{new}`")
        else:
            st.info("No files needed renaming.")
    else:
        st.error("Please enter a valid directory path.")
