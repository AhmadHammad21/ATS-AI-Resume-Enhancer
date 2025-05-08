import streamlit as st
from dotenv import load_dotenv
from src.main_page import main_page
from src.multiple_upload_page import upload_multiple_page
from src.more_features import more_features_page
from src.custom_page import custom_prompt

load_dotenv()


st.set_page_config(page_title="Candidates Matching System")

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 20% !important;
        }
        [data-testid="stSidebarContent"] {
            width: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("""
### 👥 Candidate Matching System

This tool helps recruiters quickly identify the best-fit candidates based on job descriptions and skill alignment.

#### 🔍 How to Use:

1. **Upload Candidates File**  
Supported formats: `.pdf`.

2. **Enter Job Description**  
Paste a role description or required skill set.

3. **Run Matching Algorithm**  
Click on Percentage Match button and wait for results table.

4. **Review Detailed Information**
View detailed information about each candidate strengths and weaknesses.

#### 📌 Notes:
- No data is stored or sent externally.
""")
def main():
    # selection = st.sidebar.radio("Go to", ["Main Page", "Upload Multiple CV's", "More Features", "Custom Prompt"])
    # selection = st.sidebar.radio("Go to", ["Main Page", "Upload Multiple CV's", "More Features", "Custom Prompt"])

    upload_multiple_page()
    # if selection == "Main Page":
    #     main_page()
    # if selection == "Upload Multiple CV's":
    #     upload_multiple_page()
    # if selection == "More Features":
    #     more_features_page()
    # if selection == "Custom Prompt":
    #     custom_prompt()

if __name__ == "__main__":
    main()

