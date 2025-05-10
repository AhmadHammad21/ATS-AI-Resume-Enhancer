# ATS-AI Resume Enhancer

A modern web application that helps recruiters analyze resumes against job descriptions using AI. The application provides a clean interface for uploading multiple resumes and getting detailed analysis of how well each candidate matches the job requirements.

## Features

- Modern, responsive UI built with React
- Multiple resume upload support
- AI-powered resume analysis
- Detailed matching percentage and analysis
- Clean and intuitive user interface
- FastAPI backend with automatic API documentation
- Async processing for better performance

## Project Structure

```
ATS-AI-Resume-Enhancer/
├── frontend/               # React frontend application
│   ├── public/
│   └── src/
├── backend/               # FastAPI backend application
│   ├── src/
│   └── uploads/          # Temporary storage for uploaded files
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the backend directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

6. Start the backend server:
   ```bash
   uvicorn app:app --reload
   ```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage

1. Enter the job description in the text area
2. Upload one or more resumes (PDF format)
3. Click "Analyze Resumes" to start the analysis
4. View the results showing match percentages and detailed analysis for each resume

## Technologies Used

- Frontend:
  - React
  - Material-UI
  - Axios

- Backend:
  - FastAPI
  - OpenAI API
  - PyPDF2
  - Pydantic
  - Uvicorn

## License

MIT
