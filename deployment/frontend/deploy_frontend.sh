
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
