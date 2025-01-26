# Document Management System

## Overview

This project is a lightweight document management system that allows users to upload, view, and manage documents (PDF/DOCX). The system integrates a Large Language Model (LLM) for document categorization and summarization. The application is built using modern full-stack technologies and deployed on AWS.

## Key Features

- **Frontend:** A React-based user interface for uploading documents, viewing metadata, and deleting documents.
- **Backend:** A FastAPI-based backend for handling document uploads, metadata extraction, and LLM integration.
- **LLM Integration:** Hugging Face's Inference API is used to categorize documents and generate summaries.
- **AWS Deployment:** The backend is deployed using AWS Lambda, S3, and API Gateway. The frontend is hosted on AWS S3.

## Key Decisions

1. **Frontend Framework:** React was chosen for its simplicity, flexibility, and rich ecosystem.
2. **Backend Framework:** FastAPI was selected for its performance, ease of use, and built-in support for asynchronous operations.
3. **LLM Integration:** Hugging Face's Inference API was used for its state-of-the-art natural language processing capabilities.
4. **AWS Services:** AWS Lambda, S3, and API Gateway were chosen for their scalability, cost-effectiveness, and ease of integration.

## Improvements and Fixes

- **CORS Configuration:** Properly configured CORS middleware to allow requests from the frontend.
- **File Upload Handling:** Improved file upload handling for `.pdf` and `.docx` files using `PyPDF2` and `python-docx`.
- **LLM Integration:** Switched to `google/flan-t5-large` for better instruction-following capabilities.
- **Error Handling:** Added robust error handling for file uploads, text extraction, and LLM API responses.
- **Dynamic Categorization:** The LLM now dynamically suggests category labels based on the document content.
- **Improved Prompts:** Refined prompts for categorization and summarization to ensure the LLM responds with only the requested information.

## Setup Instructions

### Local Development

#### Frontend
1. Navigate to the `frontend` folder:
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
4. Access the frontend at `http://localhost:3000`.

#### Backend
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

### AWS Deployment

#### Backend
1. Navigate to the `deployment/aws` folder:
   ```bash
   cd deployment/aws
   ```
2. Make the deployment script executable:
   ```bash
   chmod +x deploy_backend.sh
   ```
3. Run the deployment script:
   ```bash
   ./deploy_backend.sh
   ```

#### Frontend
1. Navigate to the `deployment/frontend` folder:
   ```bash
   cd deployment/frontend
   ```
2. Make the deployment script executable:
   ```bash
   chmod +x deploy_frontend.sh
   ```
3. Run the deployment script:
   ```bash
   ./deploy_frontend.sh
   ```

## Folder Structure

```
document_management_system/
├── frontend/               # React frontend code
├── backend/                # FastAPI backend code
├── deployment/             # Deployment scripts for AWS
│   ├── aws/                # Backend deployment scripts
│   └── frontend/           # Frontend deployment scripts
├── synthetic_data/         # Synthetic documents for testing
└── README.md               # Project documentation
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
