from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import os
from src.utils import get_openai_response, input_pdf_text
import re
from pydantic import BaseModel

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
    analysis: str

def extract_name_from_response(response: str) -> str:
    match = re.search(r"\(START_NAME_TAG (.*?) END_NAME_TAG\)", response)
    return match.group(1) if match else "N/A"

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
                You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
                your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
                the job description. First the output should come as percentage and then keywords missing and last final thoughts.
            """
            
            response = get_openai_response(input_prompt, pdf_content, job_description)
            
            # Extract percentage from response
            match = re.search(r"(\d{1,3})\s*%", response)
            percentage = match.group(1) + "%" if match else "N/A"
            
            name = extract_name_from_response(response)
            
            results.append(AnalysisResult(
                fileName=file.filename,
                candidateName=name,
                matchPercentage=percentage,
                analysis=response
            ))
            
        except Exception as e:
            print(f"Error processing {file.filename}: {str(e)}")
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
