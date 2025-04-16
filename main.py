from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from PyPDF2 import PdfReader
import re
from io import BytesIO
from src.utils import get_openai_response
from src.multiple_upload_page import extract_name_from_response, remove_name_from_response

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can call this API

# Helper functions (you can define these based on your original code)
def input_pdf_text(file):
    # This function reads the PDF and returns its text content
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

input_prompt = """
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
    your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

def extract_name_from_response(response: str) -> str:
    match = re.search(r"\(START_NAME_TAG (.*?) END_NAME_TAG\)", response)
    return match.group(1) if match else "N/A"

def remove_name_from_response(response: str) -> str:
    return re.sub(r"\(START_NAME_TAG (.*?) END_NAME_TAG\)", "", response)

@app.route('/', methods=['GET'])
def welcome():
    return jsonify({"message": "Health Check"})
   

@app.route('/upload', methods=['POST'])
def upload_files():
    print("🔵 Request received")
    print("Form data:")
    print(request.form)     # job_description
    print("Files:")
    print(request.files)    # list_files[]
    job_description = request.form.get("job_description")
    print(job_description)
    if not job_description:
        return jsonify({"error": "Job description is required."}), 400

    files = request.files.getlist("list_files")
    print("files")
    print(files)
    # Get the list of uploaded files
    if 'list_files' not in request.files:
        return jsonify({"error": "No files uploaded."}), 400

    # uploaded_files = request.files.getlist('list_files')
    print(files)

    if not files:
        return jsonify({"error": "Please upload at least one file."}), 400

    # Initialize variables for processing
    results = []
    names = []
    percentage_matches = []
    responses_dict = {}

    # Process each file
    for file in files[:15]:  # Limit to 15 files
        # Read the PDF content
        pdf_content = input_pdf_text(file)
        response = get_openai_response(input_prompt, pdf_content, job_description)
        responses_dict[file.filename] = response

        # Extract match percentage using regex
        match = re.search(r"(\d{1,3})\s*%", response)
        percentage = match.group(1) + "%" if match else "N/A"

        # Extract name from the response
        name = extract_name_from_response(response)

        names.append(name)
        percentage_matches.append(percentage)

        results.append({
            "Resume": file.filename,
            "Candidate Name": name,
            "Match %": percentage
        })

    # Create DataFrame from results
    df = pd.DataFrame({
        "File Name": list(responses_dict.keys()),
        "Candidate Name": names,
        "Match %": percentage_matches,
    })

    # Sort the DataFrame by "Match %"
    df = df.sort_values("Match %", ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1

    # Convert DataFrame to JSON
    df_json = df.to_dict(orient='records')
    print(f"df_json: {df_json}")

    # Prepare the final response with detailed results
    detailed_results = []
    for file_name, response in responses_dict.items():
        detailed_results.append({
            "Candidate Name": extract_name_from_response(response),
            "File Name": file_name,
            "Response Text": remove_name_from_response(response)
        })

    return jsonify({
        "summary_table": df_json,
        "detailed_results": detailed_results
    })


if __name__ == '__main__':
    app.run(debug=True)
