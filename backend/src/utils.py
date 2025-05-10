import os
import PyPDF2 as pdf
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
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
        system_prompt = """You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
        Your task is to:
        1. Extract the candidate's full name from the resume
        2. Evaluate the resume against the job description
        3. Provide a detailed analysis
        
        Format your response exactly as follows:
        [Full Name]
        Percentage of Match: [X]%
        
        Keywords Missing:
        - [Keyword 1]
        - [Keyword 2]
        ...
        
        Final Thoughts:
        [Your analysis]"""

        user_prompt = f"""
        Resume:
        {resume_text}
        
        Job Description:
        {job_description}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0
        )
        
        result = response.choices[0].message.content.strip()
        logger.debug(f"OpenAI response: {result}")
        
        return result
    except Exception as e:
        logger.error(f"Error getting OpenAI response: {str(e)}")
        return "Error analyzing resume. Please try again."