"""
process_file.py — Part 2: one file of package descriptions, uploaded.

A Streamlit app that accepts an uploaded text file with one package description
per line, shows the total for every line, and writes the parsed packages to a
JSON file in the `data/` folder — `data/packaging1.txt` in, `data/packaging1.json`
out.

New here: an uploaded file arrives as **bytes**, not text, so it has to be
decoded before it can be split into lines. And a text file usually ends with a
newline, so the last "line" is empty and must be skipped rather than parsed.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_file
"""

import json

import streamlit as st

from packaging_parser import calc_total_units, get_unit, parse_packaging

st.title("Process File of Packages")

package_file = st.file_uploader("Upload a package file", key="package_file")

if package_file is not None:
    text = package_file.getvalue().decode("utf-8")
    lines = text.splitlines()
    packages = []

    for line in lines:
        package_text = line.strip()
        if not package_text:
            continue

        package = parse_packaging(package_text)
        total = calc_total_units(package)
        unit = get_unit(package)
        packages.append(package)
        st.info(f"{package_text} ➡️ Total 📦 Size: {total} {unit}")

    output_name = package_file.name.replace(".txt", ".json")
    with open(f"data/{output_name}", "w", encoding="utf-8") as json_file:
        json.dump(packages, json_file)

    st.success(f"{len(packages)} packages written to data/{output_name}")
