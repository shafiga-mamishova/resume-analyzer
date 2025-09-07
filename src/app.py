# TODO: Streamlit for UI

import streamlit as st
import resume_parser as rp
import similarity as sim

st.title("Resume Analyzer",)

col1,col2=st.columns(2)

with col1:
    job_text=st.text_area("Job Description")

with col2:
    resume=st.file_uploader("Upload Your Resume", type=["pdf"])

if resume is not None:
    resume_text=rp.parse(resume)
    st.success("PDF processed!")
    if job_text is not None:
        score=round((sim.matching_score(job_text,resume_text))*100)
        st.write(score)
        st.write(sim.missing_keywords(job_text,resume_text))