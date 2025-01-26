
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
