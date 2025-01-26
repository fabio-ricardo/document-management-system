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
"""
with open(os.path.join(backend_folder, "requirements.txt"), "w") as f:
    f.write(requirements_txt)

# Create main.py
main_py = """
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid

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

    # Generate metadata
    document_id = str(uuid.uuid4())
    title = file.filename
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    category = "Uncategorized"  # Placeholder for LLM integration
    summary = "No summary available."  # Placeholder for LLM integration

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

3. Start the FastAPI server:
   ```bash
   python main.py
   ```

4. The backend will be available at `http://localhost:8000`.

## API Endpoints

- **POST /upload**: Upload a document (PDF or DOCX).
- **GET /documents**: Fetch a list of uploaded documents with metadata.
- **DELETE /delete/{document_id}**: Delete a document by ID.
"""
with open(os.path.join(backend_folder, "README.md"), "w") as f:
    f.write(readme)

print("Backend code and files generated successfully!")