import os
import PyPDF2 as pdf
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_text(filepath: str) -> str:
    """
    Read and extract text from a PDF file.
    
    Args:
        filepath (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_openai_response(prompt: str, resume_text: str, job_description: str) -> str:
    """
    Get analysis from OpenAI API based on resume and job description.
    
    Args:
        prompt (str): The system prompt for the analysis
        resume_text (str): The text content of the resume
        job_description (str): The job description to match against
        
    Returns:
        str: The analysis response from OpenAI
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}"}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting OpenAI response: {str(e)}")
        return "Error analyzing resume. Please try again."