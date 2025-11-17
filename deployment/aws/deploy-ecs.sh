#!/bin/bash
# AWS ECS Deployment Script

set -e

# Configuration
AWS_REGION=${AWS_REGION:-"us-east-1"}
CLUSTER_NAME="ai-llm-cluster"
SERVICE_NAME="ai-llm-api"
TASK_FAMILY="ai-llm-task"
IMAGE_TAG=${1:-"latest"}
ECR_REPOSITORY="123456789012.dkr.ecr.$AWS_REGION.amazonaws.com/ai-llm"

echo "🚀 Deploying to AWS ECS"
echo "Region: $AWS_REGION"
echo "Cluster: $CLUSTER_NAME"
echo "Image: $ECR_REPOSITORY:$IMAGE_TAG"

# Build and push Docker image to ECR
echo "📦 Building Docker image..."
docker build -t ai-llm:$IMAGE_TAG .

# Login to ECR
echo "🔐 Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin $ECR_REPOSITORY

# Tag and push
echo "📤 Pushing image to ECR..."
docker tag ai-llm:$IMAGE_TAG $ECR_REPOSITORY:$IMAGE_TAG
docker push $ECR_REPOSITORY:$IMAGE_TAG

# Update task definition
echo "📝 Updating task definition..."
TASK_DEFINITION=$(aws ecs describe-task-definition --task-definition $TASK_FAMILY --region $AWS_REGION)

NEW_TASK_DEF=$(echo $TASK_DEFINITION | jq --arg IMAGE "$ECR_REPOSITORY:$IMAGE_TAG" \
  '.taskDefinition | .containerDefinitions[0].image = $IMAGE | del(.taskDefinitionArn) | del(.revision) | del(.status) | del(.requiresAttributes) | del(.compatibilities) | del(.registeredAt) | del(.registeredBy)')

NEW_TASK_INFO=$(aws ecs register-task-definition \
  --region $AWS_REGION \
  --cli-input-json "$NEW_TASK_DEF")

NEW_REVISION=$(echo $NEW_TASK_INFO | jq -r '.taskDefinition.revision')

echo "✅ New task definition revision: $NEW_REVISION"

# Update service
echo "🔄 Updating ECS service..."
aws ecs update-service \
  --region $AWS_REGION \
  --cluster $CLUSTER_NAME \
  --service $SERVICE_NAME \
  --task-definition $TASK_FAMILY:$NEW_REVISION \
  --force-new-deployment

echo "⏳ Waiting for service to stabilize..."
aws ecs wait services-stable \
  --region $AWS_REGION \
  --cluster $CLUSTER_NAME \
  --services $SERVICE_NAME

echo "✅ Deployment complete!"
echo "Service: $SERVICE_NAME"
echo "Task Definition: $TASK_FAMILY:$NEW_REVISION"
