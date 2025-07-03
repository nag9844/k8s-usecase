#!/bin/bash

# Monitoring setup script
set -e

echo "Setting up monitoring for microservice application..."

# Apply monitoring namespace and configurations
kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f grafana-deployment.yaml

# Wait for deployments to be ready
echo "Waiting for Prometheus to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/prometheus -n monitoring

echo "Waiting for Grafana to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/grafana -n monitoring

# Get service URLs
echo ""
echo "Monitoring setup complete!"
echo ""
echo "Access URLs:"
echo "============"

PROMETHEUS_URL=$(kubectl get svc prometheus -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
GRAFANA_URL=$(kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

if [ -z "$PROMETHEUS_URL" ]; then
    echo "Prometheus: http://$(kubectl get svc prometheus -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):9090"
else
    echo "Prometheus: http://$PROMETHEUS_URL:9090"
fi

if [ -z "$GRAFANA_URL" ]; then
    echo "Grafana: http://$(kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):3000"
else
    echo "Grafana: http://$GRAFANA_URL:3000"
fi

echo ""
echo "Grafana Credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "To port-forward instead of using LoadBalancer:"
echo "kubectl port-forward -n monitoring svc/prometheus 9090:9090"
echo "kubectl port-forward -n monitoring svc/grafana 3000:3000"