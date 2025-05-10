import streamlit as st
from src.utils import get_gemini_repsonse, input_pdf_text


def custom_prompt():
    st.header("Custom Prompt")
    input_text = st.text_area("Job Description: ", key="input")
    uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

    input_prompt = st.text_area("Input Prompt: ", key="input_prompt", value="Does this resume fit the Job Description")

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")

    submit = st.button("Apply")

    if submit:
        if uploaded_file is not None:
            pdf_content = input_pdf_text(uploaded_file)
            response = get_gemini_repsonse(input_prompt, pdf_content, input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please upload the resume")
