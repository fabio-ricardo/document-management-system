import os

# Define the folder structure
deployment_folder = "deployment"
aws_folder = os.path.join(deployment_folder, "aws")
frontend_folder = os.path.join(deployment_folder, "frontend")

# Create folders
os.makedirs(aws_folder, exist_ok=True)
os.makedirs(frontend_folder, exist_ok=True)

# Create AWS deployment script (backend)
aws_deploy_sh = """
#!/bin/bash

# Variables
AWS_REGION="us-east-1"
S3_BUCKET_NAME="document-management-system-$(openssl rand -hex 6)"
LAMBDA_FUNCTION_NAME="document-management-backend"
API_GATEWAY_NAME="document-management-api"

# Install dependencies
echo "Installing dependencies..."
pip install -r ../backend/requirements.txt -t .

# Package the backend code
echo "Packaging backend code..."
zip -r lambda_function.zip .

# Create S3 bucket
echo "Creating S3 bucket..."
aws s3api create-bucket --bucket $S3_BUCKET_NAME --region $AWS_REGION

# Upload Lambda function
echo "Uploading Lambda function..."
aws lambda create-function \
    --function-name $LAMBDA_FUNCTION_NAME \
    --runtime python3.9 \
    --handler main.handler \
    --zip-file fileb://lambda_function.zip \
    --role arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:role/lambda-execution-role \
    --region $AWS_REGION

# Create API Gateway
echo "Creating API Gateway..."
API_ID=$(aws apigateway create-rest-api --name $API_GATEWAY_NAME --region $AWS_REGION --query 'id' --output text)

# Deploy API Gateway
echo "Deploying API Gateway..."
aws apigateway create-deployment --rest-api-id $API_ID --stage-name prod --region $AWS_REGION

echo "Backend deployment complete!"
"""
with open(os.path.join(aws_folder, "deploy_backend.sh"), "w") as f:
    f.write(aws_deploy_sh)

# Create frontend deployment script
frontend_deploy_sh = """
#!/bin/bash

# Variables
AWS_REGION="us-east-1"
S3_BUCKET_NAME="document-management-frontend-$(openssl rand -hex 6)"

# Build the frontend
echo "Building frontend..."
cd ../frontend
npm install
npm run build

# Create S3 bucket
echo "Creating S3 bucket..."
aws s3api create-bucket --bucket $S3_BUCKET_NAME --region $AWS_REGION

# Upload frontend files
echo "Uploading frontend files..."
aws s3 cp build/ s3://$S3_BUCKET_NAME/ --recursive

# Enable static website hosting
echo "Enabling static website hosting..."
aws s3 website s3://$S3_BUCKET_NAME/ --index-document index.html --error-document index.html

echo "Frontend deployment complete!"
echo "Access your application at: http://$S3_BUCKET_NAME.s3-website-$AWS_REGION.amazonaws.com"
"""
with open(os.path.join(frontend_folder, "deploy_frontend.sh"), "w") as f:
    f.write(frontend_deploy_sh)

# Create README.md
readme = """
# Deployment Instructions

## Backend Deployment (AWS Lambda, S3, API Gateway)

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

4. Follow the on-screen instructions to deploy the backend to AWS Lambda, S3, and API Gateway.

## Frontend Deployment (AWS S3)

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

4. Follow the on-screen instructions to deploy the frontend to AWS S3.

## Notes

- Replace `<YOUR_AWS_ACCOUNT_ID>` in the backend deployment script with your actual AWS account ID.
- Ensure you have the AWS CLI installed and configured with the necessary permissions.
"""
with open(os.path.join(deployment_folder, "README.md"), "w") as f:
    f.write(readme)

print("AWS deployment code and files generated successfully!")