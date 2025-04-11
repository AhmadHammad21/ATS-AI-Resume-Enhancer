import os
import PyPDF2 as pdf
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

def get_openai_response(input_text, pdf_content, prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": input_text},
        {"role": "user", "content": pdf_content},
        {"role": "user", "content": prompt},
        {"role": "user", "content": "Put the name of the CV inside a (START_NAME_TAG END_NAME_TAG)"}
    ]

    response = client.responses.create(
        model="gpt-4o-mini",  # or use "gpt-4" or "gpt-4o" if you have access
        input=messages,
        temperature=0.7  # Adjust based on how creative or strict you want the response
    )

    return response.output_text