
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
