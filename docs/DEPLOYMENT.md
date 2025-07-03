# Flask Application Deployment Guide

This guide covers deploying the Flask application with mysql using Docker and Kubernetes.


## Prerequisites

1. **Kubernetes Cluster**: EKS cluster with IRSA configured
2. **Docker Registry**: ECR or Docker Hub access
32. **Domain**: DNS domain for ingress (optional)

## Build and Push Docker Image

### Using AWS ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name flask-app --region ap-south-1

# Get login token
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com

# Build image
docker build -t flask-app:latest .

# Tag for ECR
docker tag flask-app:latest ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/flask-app:latest

# Push to ECR
docker push ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/flask-app:latest
```

### Using Docker Hub

```bash
# Build image
docker build -t your-username/flask-app:latest .

# Push to Docker Hub
docker push your-username/flask-app:latest
```

## Kubernetes Deployment

### 1. Update Configuration

Edit the Kubernetes manifests with your specific values:

**k8s/secret.yaml**:
```yaml
stringData:
  DB_SECRET_NAME: "your-project/prod/aurora/credentials"  # From Terraform output
  AWS_REGION: "ap-south-1"
```

**k8s/serviceaccount.yaml**:
```yaml
annotations:
  eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/your-aurora-access-role  # From Terraform output
```

**k8s/deployment.yaml**:
```yaml
image: ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/flask-app:latest  # Your image
```

**k8s/ingress.yaml**:
```yaml
- host: your-domain.com  # Your domain
```

### 2. Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/

# Or apply in order
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/config-map.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml
kubectl apply -f k8s/flask-pdb.yaml
```

### 3. Verify Deployment

```bash
# Check namespace
kubectl get all -n flask-app

# Check pods
kubectl get pods -n flask-app

# Check logs
kubectl logs -f deployment/flask-app -n flask-app

```

## Configuration Details

### Environment Variables

The application uses these environment variables:

- `FLASK_ENV`: Flask environment (production)



### Health Checks

The application provides health checks:

- **Endpoint**: `/health`
- **Liveness Probe**: Checks if app is running
- **Readiness Probe**: Checks if app can serve traffic

### Monitoring

Prometheus metrics are available:

- **Endpoint**: `/metrics`
- **Service**: `flask-app-metrics`
- **Metrics**: Request count, duration, errors, etc.

## Scaling and Performance

### Horizontal Pod Autoscaler (HPA)

The HPA automatically scales based on:

- **CPU Usage**: Target 70%
- **Memory Usage**: Target 80%
- **Min Replicas**: 3
- **Max Replicas**: 10

### Resource Limits

Each pod has resource limits:

- **CPU Request**: 250m
- **CPU Limit**: 500m
- **Memory Request**: 256Mi
- **Memory Limit**: 512Mi


## Security


### Secrets Management

- **AWS Secrets Manager**: Database credentials
- **Kubernetes Secrets**: Application secrets
- **IAM Roles**: Least privilege access

### Container Security

- **Non-root User**: Application runs as non-root
- **Read-only Filesystem**: Minimal write access
- **Security Context**: Restricted capabilities

## Troubleshooting

### Common Issues

1. **Pod CrashLoopBackOff**
   ```bash
   kubectl describe pod POD_NAME -n flask-app
   kubectl logs POD_NAME -n flask-app
   ```


2. **Health Check Failures**
   ```bash
   # Test health endpoint
   kubectl port-forward pod/POD_NAME 5000:5000 -n flask-app
   curl http://localhost:5000/health
   ```

### Useful Commands

```bash
# Scale deployment
kubectl scale deployment flask-app --replicas=5 -n flask-app

# Update image
kubectl set image deployment/flask-app flask-app=new-image:tag -n flask-app

# Check HPA status
kubectl get hpa -n flask-app

# View events
kubectl get events -n flask-app --sort-by='.lastTimestamp'

# Access application logs
kubectl logs -f deployment/flask-app -n flask-app

# Execute into pod
kubectl exec -it deployment/flask-app -n flask-app -- /bin/bash
```

## Production Considerations

### High Availability

- **Multi-AZ Deployment**: Spread pods across AZs
- **Load Balancing**: Ingress controller load balancing

### Monitoring and Alerting

- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **AlertManager**: Alert notifications

### Backup and Recovery

- **Database Backups**: Aurora automated backups
- **Application State**: Stateless application design
- **Configuration Backup**: Kubernetes manifest versioning

### Performance Optimization

- **Connection Pooling**: Efficient database connections
- **Caching**: Redis for session storage (optional)
- **CDN**: CloudFront for static assets
- **Database Optimization**: Query optimization and indexing

This deployment provides a production-ready, scalable, and secure Flask application with Aurora DB integration.