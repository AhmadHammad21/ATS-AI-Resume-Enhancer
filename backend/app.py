from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import os
from src.utils import get_openai_response, input_pdf_text
import re
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ATS Resume Analyzer API",
    description="API for analyzing resumes against job descriptions using AI",
    version="1.0.0"
)

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class AnalysisResult(BaseModel):
    fileName: str
    candidateName: str
    matchPercentage: str
    details: str

def extract_name_from_response(response: str) -> str:
    """
    Extract candidate name from the response using multiple patterns.
    """
    logger.debug(f"Raw response for name extraction: {response}")
    
    # Try to find name in square brackets
    bracket_match = re.search(r"\[(.*?)\]", response)
    if bracket_match:
        name = bracket_match.group(1).strip()
        logger.debug(f"Found name in brackets: {name}")
        return name

    # Try to find name in the format (START_NAME_TAG name END_NAME_TAG)
    name_tag_match = re.search(r"\(START_NAME_TAG\s*(.*?)\s*END_NAME_TAG\)", response)
    if name_tag_match:
        name = name_tag_match.group(1).strip()
        logger.debug(f"Found name in tags: {name}")
        return name

    # Try to find name in the format "Candidate Name: name"
    name_label_match = re.search(r"Candidate Name:\s*(.*?)(?:\n|$)", response)
    if name_label_match:
        name = name_label_match.group(1).strip()
        logger.debug(f"Found name in label: {name}")
        return name

    # Try to find name at the beginning of the response
    first_line = response.split('\n')[0].strip()
    if first_line and not first_line.startswith(('Percentage', 'Keywords', 'Final')):
        logger.debug(f"Found name in first line: {first_line}")
        return first_line

    logger.debug("No name found in response")
    return "N/A"

def format_analysis_response(response: str) -> str:
    """
    Format the analysis response to remove name tags and clean up the text.
    """
    logger.debug(f"Raw response for formatting: {response}")
    
    # Remove name tags
    response = re.sub(r"\(START_NAME_TAG.*?END_NAME_TAG\)", "", response)
    response = re.sub(r"\[.*?\]", "", response)
    
    # Clean up extra whitespace and newlines
    response = re.sub(r'\n\s*\n', '\n\n', response)
    formatted = response.strip()
    
    logger.debug(f"Formatted response: {formatted}")
    return formatted

@app.post("/upload", response_model=List[AnalysisResult])
async def analyze_resumes(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    """
    Analyze multiple resumes against a job description.
    
    Args:
        job_description: The job description to match against
        resumes: List of PDF resume files
        
    Returns:
        List of analysis results for each resume
    """
    if not resumes:
        raise HTTPException(status_code=400, detail="No resume files uploaded")

    results = []
    
    for file in resumes:
        if not file.filename.lower().endswith('.pdf'):
            continue

        try:
            # Save file temporarily
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            with open(filepath, "wb") as buffer:
                content = await file.read()
                buffer.write(content)

            # Process the resume
            pdf_content = input_pdf_text(filepath)
            
            input_prompt = """
                You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
                First, extract the candidate's full name from the resume and format it as: [Full Name]
                Then, evaluate the resume against the provided job description and provide:
                1. The percentage of match
                2. Keywords missing from the resume
                3. Final thoughts on the match
                
                Format your response as:
                [Full Name]
                Percentage of Match: [X]%
                
                Keywords Missing:
                - [Keyword 1]
                - [Keyword 2]
                ...
                
                Final Thoughts:
                [Your analysis]
            """
            
            response = get_openai_response(input_prompt, pdf_content, job_description)
            logger.debug(f"OpenAI response for {file.filename}: {response}")
            
            # Extract percentage from response
            match = re.search(r"(\d{1,3})\s*%", response)
            percentage = match.group(1) + "%" if match else "N/A"
            logger.debug(f"Extracted percentage: {percentage}")
            
            name = extract_name_from_response(response)
            logger.debug(f"Extracted name: {name}")
            
            formatted_response = format_analysis_response(response)
            logger.debug(f"Formatted response: {formatted_response}")
            
            results.append(AnalysisResult(
                fileName=file.filename,
                candidateName=name,
                matchPercentage=percentage,
                details=formatted_response
            ))
            
        except Exception as e:
            logger.error(f"Error processing {file.filename}: {str(e)}")
            continue
        finally:
            # Clean up the uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)

    if not results:
        raise HTTPException(status_code=400, detail="No valid resumes were processed")

    return JSONResponse(
        content=[result.dict() for result in results],
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Credentials": "true",
        }
    )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "ATS Resume Analyzer API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
