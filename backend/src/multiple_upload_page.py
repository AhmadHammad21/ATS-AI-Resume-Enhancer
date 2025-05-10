import streamlit as st
import pandas as pd
from src.utils import get_openai_response, input_pdf_text
import re


def upload_multiple_page():
    st.header("Candidates Matching System")
    input_text = st.text_area("Job Description: ", key="input")
    uploaded_files = st.file_uploader("Upload your resume (PDF)...", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        st.write(f"{len(uploaded_files)} PDF(s) uploaded successfully.")

    # submit1 = st.button("Tell Me About the Resume")

    # submit2 = st.button("Keypoints in Resume")

    if "responses_dict" not in st.session_state:
        st.session_state.responses_dict = {}

    submit3 = st.button("Percentage Match")

    show_more = st.button("Show Detailed Information")


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

    
    # if submit1:
    #     if uploaded_file is not None:
    #         pdf_content = input_pdf_text(uploaded_file)
    #         response = get_openai_response(input_prompt1, pdf_content, input_text)
    #         st.subheader("The Repsonse is")
    #         st.write(response)
    #     else:
    #         st.write("Please upload the resume")

    # elif submit2:
    #     if uploaded_file is not None:
    #         pdf_content = input_pdf_text(uploaded_file)
    #         response = get_openai_response(input_prompt2, pdf_content, input_text)
    #         st.subheader("The Repsonse is")
    #         st.write(response)
    #     else:
    #         st.write("Please upload the resume")

    # elif submit3:
    #     if uploaded_file is not None:
    #         pdf_content = input_pdf_text(uploaded_file)
    #         response = get_openai_response(input_prompt3, pdf_content, input_text)
    #         st.subheader("The Repsonse is")
    #         st.write(response)
    #     else:
    #         st.write("Please upload the resume")

    if submit3:
        if not uploaded_files:
            st.warning("Please upload at least one resume.")
            return

        results = []
        names = []
        percentage_matches = []
        responses_dict = {}

        with st.spinner("Evaluating resumes..."):
            for file in uploaded_files[:15]:  # Limit to 15
                # print(file)
                pdf_content = input_pdf_text(file)
                response = get_openai_response(input_prompt3, pdf_content, input_text)
                responses_dict[file.name] = response

                st.session_state.responses_dict = responses_dict
                
                # Try extracting percentage from response
                match = re.search(r"(\d{1,3})\s*%", response)
                percentage = match.group(1) + "%" if match else "N/A"

                name = extract_name_from_response(response=response)

                names.append(name)
                percentage_matches.append(percentage)
                st.session_state.names = names
            
                results.append({
                    "Resume": file.name,
                    "Candidate Name": name,
                    "Match %": percentage
                })

        df = pd.DataFrame({
            "File Name": list(responses_dict.keys()),
            "Candidate Name": names,
            "Match %": percentage_matches,
        })

        df = df.sort_values("Match %", ascending=False)
        df = df.reset_index(drop=True)
        df.index = df.index + 1

        st.session_state.response_df = df

    if "response_df" in st.session_state:
        st.subheader("📊 Summary Table")
        st.dataframe(st.session_state.response_df)


    if show_more:
        if st.session_state.get("responses_dict"):
            st.subheader("Detailed Results")
            i = 0
            for file_name, response in st.session_state.responses_dict.items():
                st.markdown(f"###### Candidate Name: {extract_name_from_response(response)} 📄 File Name: {file_name}")
                st.markdown(remove_name_from_response(response))
                i += 1
        else:
            st.info("No results found. Please click **Percentage Match** first for analysis.")



def extract_name_from_response(response: str) -> str:
    match = re.search(r"\(START_NAME_TAG (.*?) END_NAME_TAG\)", response)
    return match.group(1) if match else "N/A"


def remove_name_from_response(response: str) -> str:
    text = re.sub(r"\(START_NAME_TAG (.*?) END_NAME_TAG\)", "", response)
    return text