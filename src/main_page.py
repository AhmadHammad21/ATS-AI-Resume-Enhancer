import streamlit as st
from src.utils import get_gemini_repsonse, input_pdf_text


def main_page():
    st.header("ATS Tracking System")
    input_text = st.text_area("Job Description: ", key="input")
    uploaded_file = st.file_uploader("Upload your resume (PDF)...",type=["pdf"])

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")

    submit1 = st.button("Tell Me About the Resume")

    submit2 = st.button("Keypoints in Resume")

    submit3 = st.button("Percentage Match")

    input_prompt1 = """
        You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
        Please share your professional evaluation on whether the candidate's profile aligns with the role. 
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """

    # Keypoints in my Resume
    input_prompt2 = """
        Analyze a resume and job description. Identify keywords and skills from the job description absent in the resume.
        Prioritize based on frequency and relevance to the job. Provide suggestions for integrating these keywords into the resume,
        emphasizing achievements and quantifiable results.
    """

    input_prompt3 = """
        You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
        your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
        the job description. First the output should come as percentage and then keywords missing and last final thoughts.
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

