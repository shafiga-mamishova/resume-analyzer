# TODO: Streamlit for UI

import streamlit as st
import resume_parser as rp

st.title("Resume Analyzer",)

col1,col2=st.columns(2)

with col1:
    st.text_area("Job Description")

with col2:
    resume=st.file_uploader("Upload Your Resume", type=["pdf"])

if resume is not None:
    rp.parse(resume)
    st.success("PDF processed!")