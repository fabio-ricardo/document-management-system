from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
import requests
from dotenv import load_dotenv
from PyPDF2 import PdfReader  # For PDF text extraction
from docx import Document as DocxDocument  # For DOCX text extraction
import tempfile
import re

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Hugging Face API configuration
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models"
HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")  # Retrieve token from .env

# In-memory storage for documents (replace with a database in production)
documents = []

class DocumentMetadata(BaseModel):
    id: str
    title: str
    uploadDate: str
    category: str
    summary: str

def query_hugging_face(payload, model):
    """
    Query Hugging Face's Inference API.
    """
    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{HUGGING_FACE_API_URL}/{model}", headers=headers, json=payload)
    return response.json()

def categorize_document(content: str) -> str:
    """
    Use Hugging Face's Inference API to categorize the document.
    """
    prompt = f"""
    Analyze the following document content and suggest a category label that best describes it.
    The category should be a single word or a short phrase.
    Respond with only the category label and nothing else.
    Document Content: {content}
    """
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 20,  # Limit the response to a short label
        },
    }
    # Use a more instruction-following model like flan-t5-large
    response = query_hugging_face(payload, "google/flan-t5-large")
    
    # Extract the category label from the response
    if isinstance(response, list) and len(response) > 0:
        generated_text = response[0].get("generated_text", "").strip()
    elif isinstance(response, dict):
        generated_text = response.get("generated_text", "").strip()
    else:
        generated_text = ""
    
    # Remove the prompt and extract only the first line (category label)
    category = generated_text.replace(prompt, "").strip().split("\n")[0]
    return category if category else "other"

def summarize_document(content: str) -> str:
    """
    Use Hugging Face's Inference API to summarize the document.
    """
    prompt = f"""
    Summarize the following document content in one sentence.
    Respond with only the summary and nothing else.
    Document Content: {content}
    """
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 50,  # Limit summary to one sentence
        },
    }
    # Use a more instruction-following model like flan-t5-large
    response = query_hugging_face(payload, "google/flan-t5-large")
    
    # Extract the summary from the response
    if isinstance(response, list) and len(response) > 0:
        generated_text = response[0].get("generated_text", "").strip()
    elif isinstance(response, dict):
        generated_text = response.get("generated_text", "").strip()
    else:
        generated_text = ""
    
    # Remove the prompt and extract only the first line (summary)
    summary = generated_text.replace(prompt, "").strip().split("\n")[0]
    return summary if summary else "No summary available."

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file.
    """
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()  # Remove trailing newlines
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {str(e)}")

def extract_text_from_docx(file):
    """
    Extract text from a DOCX file.
    """
    try:
        doc = DocxDocument(file)
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"
        return text.strip()  # Remove trailing newlines
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from DOCX: {str(e)}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX files are allowed.")

    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="The file is empty.")
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        # Extract text based on file type
        if file.content_type == "application/pdf":
            with open(temp_file_path, "rb") as f:
                content = extract_text_from_pdf(f)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            with open(temp_file_path, "rb") as f:
                content = extract_text_from_docx(f)
        else:
            content = ""
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

    if not content:
        raise HTTPException(status_code=400, detail="Failed to extract text from the file. The file may be empty or unsupported.")

    # Generate metadata
    document_id = str(uuid.uuid4())
    title = file.filename
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Use Hugging Face to categorize and summarize the document
    category = categorize_document(content)
    summary = summarize_document(content)

    # Store document metadata
    document = DocumentMetadata(
        id=document_id,
        title=title,
        uploadDate=upload_date,
        category=category,
        summary=summary,
    )
    documents.append(document)

    return document

@app.get("/documents")
async def get_documents():
    return documents

@app.delete("/delete/{document_id}")
async def delete_document(document_id: str):
    global documents
    documents = [doc for doc in documents if doc.id != document_id]
    return {"message": "Document deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)