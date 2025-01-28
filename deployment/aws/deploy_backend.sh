#!/bin/bash

set -e  # Exit script on command failure
trap 'cleanup' EXIT

# Variables
AWS_REGION=${AWS_REGION:-"us-east-1"}
S3_BUCKET_NAME="document-management-system-$(openssl rand -hex 6)"
LAMBDA_FUNCTION_NAME="document-management-backend"
API_GATEWAY_NAME="document-management-api"
ROLE_NAME="lambda-execution-role"

# Functions
cleanup() {
    echo "Cleaning up resources..."
    aws s3 rb s3://$S3_BUCKET_NAME --force || true
    aws lambda delete-function --function-name $LAMBDA_FUNCTION_NAME || true
    echo "Resources cleaned up."
}

echo "Installing dependencies..."
pip3 install -r ../../backend/requirements.txt -t .

echo "Packaging backend code..."
zip -r lambda_function.zip .

echo "Creating S3 bucket..."
aws s3api create-bucket --bucket $S3_BUCKET_NAME --region $AWS_REGION

echo "Uploading Lambda function..."
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)
aws lambda create-function \
    --function-name $LAMBDA_FUNCTION_NAME \
    --runtime python3.9 \
    --handler main.handler \
    --zip-file fileb://lambda_function.zip \
    --role $ROLE_ARN \
    --region $AWS_REGION

echo "Creating API Gateway..."
API_ID=$(aws apigateway create-rest-api --name $API_GATEWAY_NAME --region $AWS_REGION --query 'id' --output text)

echo "Adding POST method to API Gateway..."
RESOURCE_ID=$(aws apigateway get-resources --rest-api-id $API_ID --query 'items[0].id' --output text)

aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method POST \
    --authorization-type "NONE"

echo "Linking POST method to Lambda function..."
aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method POST \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri "arn:aws:apigateway:$AWS_REGION:lambda:path/2015-03-31/functions/arn:aws:lambda:$AWS_REGION:615299727823:function:$LAMBDA_FUNCTION_NAME/invocations"  \

echo "Deploying API Gateway..."
aws apigateway create-deployment \
    --rest-api-id $API_ID \
    --stage-name prod \
    --region $AWS_REGION

echo "Deployment complete!"
