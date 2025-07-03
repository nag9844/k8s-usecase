# Kubernetes Microservice Project with kops

## Overview
This project demonstrates a complete Kubernetes microservice deployment following production best practices for scalability, security, and observability.

## Architecture
- **Application**: python web application with mysql backend
- **Infrastructure**: k8s deployed with kops
- **Monitoring**: Prometheus & Grafana
- **Security**: RBAC, non-root containers, security contexts
- **Networking**: Custom VPC with proper security groups

## Project Structure
```
├── app/          # Containerized application
├── app/k8s/                   # K8s manifests          
├── Monitoring/         # Monitoring setup
└── docs/                    # Documentation
```

## Quick Start
1. Follow `docs/kops-setup.md` for cluster creation
2. Deploy application using `kubectl apply -k app/k8s/`
3. Set up monitoring with `Monitoring/setup.sh`

## Prerequisites
- AWS CLI configured
- kubectl installed
- kops installed
- Docker installed