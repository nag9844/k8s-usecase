# Application Architecture

## Overview
This microservice application demonstrates enterprise-grade Kubernetes deployment patterns with comprehensive security, monitoring, and scalability features.

## Components

### Application Layer
- **Pyhton Microservice**: Main application serving HTTP requests
- **mysql**:  data store for user details
- **Init Container**: Ensures dependencies are ready before main app starts
- **Sidecar Container**: Handles log forwarding and auxiliary tasks

### Infrastructure Layer
- **Kubernetes Cluster**: Orchestration platform (deployed via kops)
- **Custom VPC**: Isolated network environment
- **Security Groups**: Network-level security controls
- **Load Balancer**: Distributes traffic across application instances

### Security Layer
- **RBAC**: Role-based access control for service accounts
- **Network Policies**: Pod-to-pod communication controls
- **Security Contexts**: Container-level security settings

### Observability Layer
- **Prometheus**: Metrics collection 
- **Grafana**: Visualization and dashboards
- **Application Metrics**: Custom metrics endpoint
- **Health Checks**: Liveness and readiness probes

## Data Flow

1. **External Traffic** → Load Balancer
2. **Load Balancer** → Kubernetes Service
3. **Service** → Application Pods (3 replicas)
4. **Application** → msql for data storage
5. **Metrics** → Prometheus for monitoring
6. **Alerts** → Grafana for visualization

## Scaling Strategy

- **Horizontal Pod Autoscaler**: Auto-scales based on CPU/memory
- **Pod Disruption Budget**: Ensures minimum availability during updates
- **Anti-Affinity Rules**: Distributes pods across nodes
- **Resource Limits**: Prevents resource starvation

## Security Model

- **Defense in Depth**: Multiple security layers
- **Least Privilege**: Minimal required permissions
- **Network Segmentation**: Isolated pod communications
- **Container Security**: Non-root users, read-only filesystems