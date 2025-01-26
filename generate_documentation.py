import os

# Define the folder structure
project_folder = "document_management_system"
os.makedirs(project_folder, exist_ok=True)

# Create README.md
readme = """
# Document Management System

## Overview

This project is a lightweight document management system that allows users to upload, view, and manage documents (PDF/DOCX). The system integrates a Large Language Model (LLM) for document categorization and summarization. The application is built using modern full-stack technologies and deployed on AWS.

## Key Features

- **Frontend:** A React-based user interface for uploading documents, viewing metadata, and deleting documents.
- **Backend:** A FastAPI-based backend for handling document uploads, metadata extraction, and LLM integration.
- **LLM Integration:** OpenAI's GPT API is used to categorize documents and generate summaries.
- **AWS Deployment:** The backend is deployed using AWS Lambda, S3, and API Gateway. The frontend is hosted on AWS S3.

## Key Decisions

1. **Frontend Framework:** React was chosen for its simplicity, flexibility, and rich ecosystem.
2. **Backend Framework:** FastAPI was selected for its performance, ease of use, and built-in support for asynchronous operations.
3. **LLM Integration:** OpenAI's GPT API was used for its state-of-the-art natural language processing capabilities.
4. **AWS Services:** AWS Lambda, S3, and API Gateway were chosen for their scalability, cost-effectiveness, and ease of integration.

## Challenges and Solutions

1. **File Upload Validation:** Ensuring only PDF and DOCX files are uploaded was achieved using FastAPI's file validation features.
2. **CORS Configuration:** CORS issues were resolved by configuring the FastAPI backend to allow requests from the frontend.
3. **LLM Integration:** Handling large document content and optimizing API calls were addressed by chunking content and caching results.
4. **AWS Deployment:** Setting up IAM roles and permissions for Lambda and S3 required careful configuration and testing.

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
"""
with open(os.path.join(project_folder, "README.md"), "w") as f:
    f.write(readme)

# Create LICENSE file
license_text = """
MIT License

Copyright (c) 2023 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
with open(os.path.join(project_folder, "LICENSE"), "w") as f:
    f.write(license_text)

print("Documentation and ReadMe generated successfully!")
