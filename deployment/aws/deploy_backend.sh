
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
aws lambda create-function     --function-name $LAMBDA_FUNCTION_NAME     --runtime python3.9     --handler main.handler     --zip-file fileb://lambda_function.zip     --role arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:role/lambda-execution-role     --region $AWS_REGION

# Create API Gateway
echo "Creating API Gateway..."
API_ID=$(aws apigateway create-rest-api --name $API_GATEWAY_NAME --region $AWS_REGION --query 'id' --output text)

# Deploy API Gateway
echo "Deploying API Gateway..."
aws apigateway create-deployment --rest-api-id $API_ID --stage-name prod --region $AWS_REGION

echo "Backend deployment complete!"
