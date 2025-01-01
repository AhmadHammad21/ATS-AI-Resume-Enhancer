import streamlit as st
from dotenv import load_dotenv
from src.main_page import main_page
from src.more_features import more_features_page
from src.custom_page import custom_prompt

load_dotenv()

st.set_page_config(page_title="ATS Resume Expert")

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Main Page", "More Features", "Custom Prompt"])

    if selection == "Main Page":
        main_page()
    if selection == "More Features":
        more_features_page()
    if selection == "Custom Prompt":
        custom_prompt()

if __name__ == "__main__":
    main()

