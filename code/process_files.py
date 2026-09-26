"""
process_files.py — Part 3: many files, one after another, with a running total.

The same job as process_file.py, but the app now remembers what it has already
done: how many files have been processed, how many packages that came to, and a
one-line summary of each file — and it keeps remembering across uploads.

That is the hard part, and it is hard for a specific reason: every interaction
reruns this whole script from the top, so an ordinary variable like
`files_processed = 0` is reset to zero on every rerun. Anything that has to
survive a rerun lives in `st.session_state` instead, and is initialised only
once — the first time the script runs.

The other trap is the uploader itself. Once a file has been chosen it stays
chosen on every rerun, so an app that processes "whenever there is a file" would
count the same file again on every interaction. Processing happens on a button
click instead: `st.button` is True only on the one rerun the click caused.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_files
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from packaging_parser import parse_packaging

if "files_processed" not in st.session_state:
    st.session_state.files_processed = 0
if "packages_processed" not in st.session_state:
    st.session_state.packages_processed = 0
if "file_summaries" not in st.session_state:
    st.session_state.file_summaries = []

st.title("Process Package Files")

package_file = st.file_uploader("Upload a package file", key="package_file")
clicked = st.button("Process file", key="process")  # True only when just clicked

if clicked and package_file is not None:
    text = package_file.getvalue().decode("utf-8")
    packages = []

    for line in text.splitlines():
        package_text = line.strip()
        if not package_text:
            continue
        packages.append(parse_packaging(package_text))

    output_name = package_file.name.replace(".txt", ".json")
    with open(f"data/{output_name}", "w", encoding="utf-8") as json_file:
        json.dump(packages, json_file)

    summary = f"{len(packages)} packages written to data/{output_name}"
    st.session_state.files_processed += 1
    st.session_state.packages_processed += len(packages)
    st.session_state.file_summaries.append(summary)

left_column, right_column = st.columns(2)
with left_column:
    st.metric("Files processed", st.session_state.files_processed)
with right_column:
    st.metric("Packages processed", st.session_state.packages_processed)

for summary in st.session_state.file_summaries:
    st.info(summary)
