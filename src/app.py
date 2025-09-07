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
        st.write("Matching score:")
        st.write(f"{score} %")
        skills_suggestions,actions_suggestions,missing = sim.suggestion(job_text,resume_text)
        st.write("**Missing Keywords:**")
        if missing:
            # st.write(", ".join(missing))
            for m in missing:
                st.write(f"- {m}")
        else:
            st.write("No missing keywords")
        st.subheader("Suggested additions")
        if skills_suggestions:
            st.write("**Skills:**")
            for s in skills_suggestions:
                st.write(f"- {s}")
        else:
            st.write("No suggestions for skills")
        if actions_suggestions:
            st.write("**Actions:**")
            for a in actions_suggestions:
                st.write(f"- {a}")
        else:
            st.write("No  suggestions for actions")