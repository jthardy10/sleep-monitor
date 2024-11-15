#!/bin/bash

# Build images
docker-compose build

# Push to registry (example for AWS ECR)
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com

docker tag sleep-monitor-backend:latest $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/sleep-monitor-backend
docker tag sleep-monitor-frontend:latest $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/sleep-monitor-frontend

docker push $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/sleep-monitor-backend
docker push $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/sleep-monitor-frontend
