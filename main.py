import json

import requests
import streamlit as st

BASE_URL = "https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/"

def load_all_subject_codes() -> dict:
    with open('./subjects.json', 'r') as f:
        s = json.load(f)
    return {item["code"]: item["name"] for item in s}

def get_paper_code(subject, paper, year, t) -> str:
    paper_code = subject + "_" + "m" + year[2:] + "_" + t.lower() + "_" + paper + "2"
    return paper_code

def get_paper_link(subject, paper, year, t) -> str:
    url = BASE_URL + get_paper_code(subject, paper, year, t) + '.pdf'
    return url

def get_code_from_name(subjects, subject_name) -> str | None:
    for code, name in subjects.items():
        if name == subject_name:
            return code
    return None

st.title('IGCSE Paper Searcher')
print(load_all_subject_codes())

pdf_bytes = None
download_name = None
subjects = load_all_subject_codes()

with st.form("paper_form"):
    subject = st.selectbox("Subject", subjects.values(), placeholder="Select a subject")
    paper_type = st.selectbox(
        "Do you want the QP or the MS?",
        ("Question Paper", "Mark Scheme"),
        placeholder="Select paper type...",
    )
    year = st.text_input("Year (e.g. 2023)")
    paper_num = st.text_input("Paper Number")

    submitted = st.form_submit_button("Submit")

if submitted:
    st.write("### 📥 Download Info:")
    st.write(f"**Subject:** {subject}")
    st.write(f"**Paper Type:** {paper_type}")
    st.write(f"**Year:** {year}")
    st.write(f"**Paper Number:** {paper_num}")

    pt = 'qp' if paper_type == 'Question Paper' else 'ms'

    scode = get_code_from_name(subjects, subject)

    url = get_paper_link(subject=scode, paper=paper_num, year=year, t=pt)
    resp = requests.get(url)

    # if an HTML file is returned, that means its the PapaCambridge main page so the file wasn't found
    if '<!DOCTYPE html>' in str(resp.content):
        st.error("Paper does not exist, please recheck your information.")

    if resp.status_code == 200:
        pdf_bytes = resp.content
        download_name = get_paper_code(subject=subject, paper=paper_num, year=year, t=pt)
    else:
        st.error("Failed to retrieve the paper, please recheck your information or reload the app. If the issue persists, file an issue.")

if pdf_bytes and download_name:
    st.download_button(
        label="📥 Download PDF",
        data=pdf_bytes,
        file_name=download_name,
        mime="application/pdf"
    )

# janky ass footer
st.markdown("""
    <hr style="margin-top:50px;">
    <div style="text-align: center; color: grey;">
        © 2025 Adit Chakraborty | Built using Streamlit
        <p>All the GCSE files are fetched from https://papacambridge.com/</p>
    </div>
""", unsafe_allow_html=True)