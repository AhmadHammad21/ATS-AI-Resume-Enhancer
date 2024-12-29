import os
import PyPDF2 as pdf
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input, pdf_content, prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""
# These prompts worked well for me:

# 1) Keypoints in my Resume
# Extract technical skills, soft skills, education details, and experience/project information directly from the resume. Only include information explicitly stated in the resume for each category.

# 2) Match with Job Description
# Given a resume and a job description, generate a table illustrating the match. Use cues to represent high, medium, and low match areas, highlighting strengths and weaknesses.

# 3) Keywords Missing in my Resume based on Job Description
# Analyze a resume and job description. Identify keywords and skills from the job description absent in the resume. Prioritize based on frequency and relevance to the job. Provide suggestions for integrating these keywords into the resume, emphasizing achievements and quantifiable results.
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response = get_gemini_repsonse(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response = get_gemini_repsonse(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")


