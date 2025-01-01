import streamlit as st
from src.utils import get_gemini_repsonse, input_pdf_text


def more_features_page():
    st.header("ATS AI Resume Enhancer")
    input_text = st.text_area("Job Description: ", key="input")
    uploaded_file = st.file_uploader("Upload your resume (PDF)...",type=["pdf"])


    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")

    submit1 = st.button("Match with Job Description")

    submit2 = st.button("Interview tip")

    submit3 = st.button("Job Market Insights")

    submit4 = st.button("Skills Gap Analysis")


    # Match with Job Description
    input_prompt1 = """
        Given a resume and a job description, generate a table illustrating the match. Use cues to represent high,
        medium, and low match areas, highlighting strengths and weaknesses.
    """

    # Interview tip
    input_prompt2 = """
        Based on the job description and the resume, provide the user with personalized tips for interview preparation.
    """

    # Job Market Insights
    input_prompt3 = """
        Provide users with insights about the current job market for similar roles, such as average salary, required experience,
        and top skills.
    """

    # Skills Gap Analysis
    input_prompt4 = """
        Provide the user with an analysis of any missing skills or qualifications based on the job description and the resume.
    """

    if submit1:
        if uploaded_file is not None:
            pdf_content = input_pdf_text(uploaded_file)
            response = get_gemini_repsonse(input_prompt1, pdf_content, input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please upload the resume")

    elif submit2:
        if uploaded_file is not None:
            pdf_content = input_pdf_text(uploaded_file)
            response = get_gemini_repsonse(input_prompt2, pdf_content, input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please upload the resume")

    elif submit3:
        if uploaded_file is not None:
            pdf_content = input_pdf_text(uploaded_file)
            response = get_gemini_repsonse(input_prompt3, pdf_content, input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please upload the resume")

    elif submit4:
        if uploaded_file is not None:
            pdf_content = input_pdf_text(uploaded_file)
            response = get_gemini_repsonse(input_prompt4, pdf_content, input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please upload the resume")


