Here are the steps to create service accounts on cluster-one and cluster-two, and generate bearer tokens for them:

For each cluster (cluster-one and cluster-two), follow these steps:

1. Create a namespace for the monitoring service account:

```bash
kubectl create namespace monitoring
```

2. Create a service account in the monitoring namespace:

```bash
kubectl create serviceaccount prometheus -n monitoring
```

3. Create a ClusterRole with the necessary permissions:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: prometheus-reader
rules:
- apiGroups: [""]
  resources:
  - nodes
  - nodes/proxy
  - services
  - endpoints
  - pods
  verbs: ["get", "list", "watch"]
- apiGroups:
  - extensions
  resources:
  - ingresses
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
EOF
```

4. Bind the ClusterRole to the service account:

```bash
kubectl create clusterrolebinding prometheus-reader-binding --clusterrole=prometheus-reader --serviceaccount=monitoring:prometheus
```

5. Create a secret for the service account token:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: prometheus-token
  namespace: monitoring
  annotations:
    kubernetes.io/service-account.name: prometheus
type: kubernetes.io/service-account-token
EOF
```

6. Retrieve the bearer token:

```bash
kubectl get secret prometheus-token -n monitoring -o jsonpath='{.data.token}' | base64 --decode
```

7. Save the bearer token securely, as you'll need it for the Prometheus configuration.

8. Get the cluster's API server address:

```bash
kubectl cluster-info | grep 'Kubernetes control plane'
```

Repeat these steps for both cluster-one and cluster-two.

After completing these steps, you'll have:
- A service account named "prometheus" in the "monitoring" namespace on each cluster
- A ClusterRole and ClusterRoleBinding giving the necessary permissions
- A bearer token for each cluster

Now, update your `prometheus-values.yaml` file with the correct API server addresses and bearer tokens:

```yaml
server:
  global:
    scrape_interval: 15s
    evaluation_interval: 15s
  persistentVolume:
    size: 8Gi
  additionalScrapeConfigs:
    - job_name: 'cluster-one-node-exporter'
      kubernetes_sd_configs:
        - api_server: https://cluster-one-api-server:6443  # Replace with actual API server address
          tls_config:
            insecure_skip_verify: true
          bearer_token: "your-cluster-one-bearer-token"  # Replace with actual token
      scheme: https
      tls_config:
        insecure_skip_verify: true
      bearer_token: "your-cluster-one-bearer-token"  # Replace with actual token
      relabel_configs:
        - source_labels: [__meta_kubernetes_node_name]
          regex: (.+)
          target_label: __metrics_path__
          replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor

    - job_name: 'cluster-two-node-exporter'
      kubernetes_sd_configs:
        - api_server: https://cluster-two-api-server:6443  # Replace with actual API server address
          tls_config:
            insecure_skip_verify: true
          bearer_token: "your-cluster-two-bearer-token"  # Replace with actual token
      scheme: https
      tls_config:
        insecure_skip_verify: true
      bearer_token: "your-cluster-two-bearer-token"  # Replace with actual token
      relabel_configs:
        - source_labels: [__meta_kubernetes_node_name]
          regex: (.+)
          target_label: __metrics_path__
          replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
```

Make sure to replace the API server addresses and bearer tokens with the actual values you obtained from each cluster.
