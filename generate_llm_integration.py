import os

# Define the folder structure
backend_folder = "backend"
api_folder = os.path.join(backend_folder, "api")
models_folder = os.path.join(backend_folder, "models")
utils_folder = os.path.join(backend_folder, "utils")

# Create folders
os.makedirs(api_folder, exist_ok=True)
os.makedirs(models_folder, exist_ok=True)
os.makedirs(utils_folder, exist_ok=True)

# Create requirements.txt
requirements_txt = """
fastapi==0.95.2
uvicorn==0.22.0
python-multipart==0.0.6
pydantic==1.10.7
python-dotenv==1.0.0
openai==0.28.0
"""
with open(os.path.join(backend_folder, "requirements.txt"), "w") as f:
    f.write(requirements_txt)

# Create utils/openai_utils.py
openai_utils_py = """
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def categorize_document(content: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that categorizes documents."},
            {"role": "user", "content": f"Categorize the following document content into one of these categories: Invoice, Contract, Report, or Other. Content: {content}"},
        ],
        max_tokens=10,
    )
    return response.choices[0].message.content.strip()

def summarize_document(content: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
            {"role": "user", "content": f"Summarize the following document content in one sentence: {content}"},
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content.strip()
"""
with open(os.path.join(utils_folder, "openai_utils.py"), "w") as f:
    f.write(openai_utils_py)

# Create main.py
main_py = """
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid
from utils.openai_utils import categorize_document, summarize_document

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# In-memory storage for documents (replace with a database in production)
documents = []

class DocumentMetadata(BaseModel):
    id: str
    title: str
    uploadDate: str
    category: str
    summary: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX files are allowed.")

    # Read file content (for LLM processing)
    content = await file.read()
    content_str = content.decode("utf-8", errors="ignore")  # Decode bytes to string

    # Generate metadata
    document_id = str(uuid.uuid4())
    title = file.filename
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Use OpenAI API to categorize and summarize the document
    category = categorize_document(content_str)
    summary = summarize_document(content_str)

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
"""
with open(os.path.join(backend_folder, "main.py"), "w") as f:
    f.write(main_py)

# Create .env file (for environment variables)
env_file = """
# Add your environment variables here
OPENAI_API_KEY=your_openai_api_key_here
"""
with open(os.path.join(backend_folder, ".env"), "w") as f:
    f.write(env_file)

# Create README.md
readme = """
# Document Management System - Backend

## Setup Instructions

1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your OpenAI API key to the `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Start the FastAPI server:
   ```bash
   python main.py
   ```

5. The backend will be available at `http://localhost:8000`.

## API Endpoints

- **POST /upload**: Upload a document (PDF or DOCX). The document will be categorized and summarized using OpenAI's GPT API.
- **GET /documents**: Fetch a list of uploaded documents with metadata.
- **DELETE /delete/{document_id}**: Delete a document by ID.
"""
with open(os.path.join(backend_folder, "README.md"), "w") as f:
    f.write(readme)

print("Backend code and files generated successfully!")