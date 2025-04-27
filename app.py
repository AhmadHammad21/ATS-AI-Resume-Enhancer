import streamlit as st
from dotenv import load_dotenv
from src.main_page import main_page
from src.multiple_upload_page import upload_multiple_page
from src.more_features import more_features_page
from src.custom_page import custom_prompt

load_dotenv()

st.set_page_config(page_title="ATS Resume Expert")

def main():
    st.sidebar.title("Navigation")
    # selection = st.sidebar.radio("Go to", ["Main Page", "Upload Multiple CV's", "More Features", "Custom Prompt"])
    selection = st.sidebar.radio("Go to", ["Upload Multiple CV's"])

    # if selection == "Main Page":
    #     main_page()
    if selection == "Upload Multiple CV's":
        upload_multiple_page()
    # if selection == "More Features":
    #     more_features_page()
    # if selection == "Custom Prompt":
    #     custom_prompt()

if __name__ == "__main__":
    main()

