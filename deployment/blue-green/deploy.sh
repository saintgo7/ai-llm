#!/bin/bash
# Blue-Green Deployment Script for Kubernetes

set -e

# Configuration
NAMESPACE="default"
BLUE_DEPLOYMENT="api-server-blue"
GREEN_DEPLOYMENT="api-server-green"
SERVICE_NAME="api-server"
NEW_IMAGE="$1"

if [ -z "$NEW_IMAGE" ]; then
  echo "Usage: $0 <new-image-tag>"
  echo "Example: $0 ai-llm:v2.0.0"
  exit 1
fi

echo "🚀 Starting Blue-Green Deployment"
echo "New image: $NEW_IMAGE"
echo "Namespace: $NAMESPACE"

# Determine current active deployment
CURRENT_DEPLOYMENT=$(kubectl get service $SERVICE_NAME -n $NAMESPACE -o jsonpath='{.spec.selector.version}')

if [ "$CURRENT_DEPLOYMENT" == "blue" ]; then
  INACTIVE_DEPLOYMENT=$GREEN_DEPLOYMENT
  INACTIVE_VERSION="green"
  ACTIVE_DEPLOYMENT=$BLUE_DEPLOYMENT
  ACTIVE_VERSION="blue"
else
  INACTIVE_DEPLOYMENT=$BLUE_DEPLOYMENT
  INACTIVE_VERSION="blue"
  ACTIVE_DEPLOYMENT=$GREEN_DEPLOYMENT
  ACTIVE_VERSION="green"
fi

echo "Current active: $ACTIVE_VERSION"
echo "Deploying to: $INACTIVE_VERSION"

# Deploy to inactive environment
echo "📦 Deploying new version to $INACTIVE_VERSION environment..."

kubectl set image deployment/$INACTIVE_DEPLOYMENT \
  api=$NEW_IMAGE \
  -n $NAMESPACE

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
kubectl rollout status deployment/$INACTIVE_DEPLOYMENT -n $NAMESPACE --timeout=5m

# Run health checks
echo "🏥 Running health checks..."
POD=$(kubectl get pods -n $NAMESPACE -l version=$INACTIVE_VERSION -o jsonpath='{.items[0].metadata.name}')

for i in {1..10}; do
  echo "Health check attempt $i..."
  if kubectl exec -n $NAMESPACE $POD -- curl -f http://localhost:5000/api/health; then
    echo "✅ Health check passed"
    break
  fi

  if [ $i -eq 10 ]; then
    echo "❌ Health checks failed"
    echo "Rolling back..."
    kubectl rollout undo deployment/$INACTIVE_DEPLOYMENT -n $NAMESPACE
    exit 1
  fi

  sleep 5
done

# Run smoke tests
echo "🧪 Running smoke tests..."
kubectl exec -n $NAMESPACE $POD -- python -m pytest tests/test_integration.py -v

# Switch traffic to new version
echo "🔄 Switching traffic to $INACTIVE_VERSION..."

kubectl patch service $SERVICE_NAME -n $NAMESPACE -p "{\"spec\":{\"selector\":{\"version\":\"$INACTIVE_VERSION\"}}}"

echo "✅ Traffic switched to $INACTIVE_VERSION"

# Monitor for issues
echo "👀 Monitoring new deployment for 30 seconds..."
sleep 30

# Check error rate
ERRORS=$(kubectl logs -n $NAMESPACE -l version=$INACTIVE_VERSION --tail=100 | grep -i error | wc -l)

if [ $ERRORS -gt 10 ]; then
  echo "⚠️  High error rate detected ($ERRORS errors)"
  echo "Rolling back to $ACTIVE_VERSION..."

  kubectl patch service $SERVICE_NAME -n $NAMESPACE -p "{\"spec\":{\"selector\":{\"version\":\"$ACTIVE_VERSION\"}}}"

  echo "❌ Deployment rolled back"
  exit 1
fi

echo "✅ Deployment successful!"
echo "New version is now serving traffic"

# Optional: Scale down old version
read -p "Scale down $ACTIVE_VERSION deployment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "📉 Scaling down $ACTIVE_VERSION..."
  kubectl scale deployment/$ACTIVE_DEPLOYMENT --replicas=0 -n $NAMESPACE
  echo "✅ Old version scaled down"
fi

echo "🎉 Blue-Green deployment complete!"
