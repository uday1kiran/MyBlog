Step 1: Prerequisites
Ensure you have the following tools installed on your local machine:
- kubectl
- helm
- helmfile

Also, make sure you have access to all three Kubernetes clusters and can switch between them using kubectl.

Step 2: Set up the directory structure
Create a new directory for your project and navigate into it:

```
mkdir k8s-monitoring
cd k8s-monitoring
```

Step 3: Create Helmfile for the monitoring cluster
Create a file named `helmfile-monitoring.yaml` in the project directory with the following content:

```yaml
repositories:
  - name: prometheus-community
    url: https://prometheus-community.github.io/helm-charts
  - name: grafana
    url: https://grafana.github.io/helm-charts

releases:
  - name: prometheus
    namespace: monitoring
    chart: prometheus-community/prometheus
    version: 15.10.1
    values:
      - prometheus-values.yaml

  - name: grafana
    namespace: monitoring
    chart: grafana/grafana
    version: 6.38.1
    values:
      - grafana-values.yaml
```

Step 4: Create value files for Prometheus and Grafana
Create `prometheus-values.yaml`:

```yaml
server:
  global:
    scrape_interval: 15s
    evaluation_interval: 15s
  persistentVolume:
    size: 8Gi
```

Create `grafana-values.yaml`:

```yaml
adminPassword: your-secure-password
persistence:
  enabled: true
  size: 5Gi
```

Step 5: Create Helmfile for clusters one and two
Create a file named `helmfile-clusters.yaml` in the project directory:

```yaml
repositories:
  - name: prometheus-community
    url: https://prometheus-community.github.io/helm-charts

releases:
  - name: node-exporter
    namespace: monitoring
    chart: prometheus-community/prometheus-node-exporter
    version: 3.3.0

  - name: kube-state-metrics
    namespace: monitoring
    chart: prometheus-community/kube-state-metrics
    version: 4.20.2
```

Step 6: Install components on the monitoring cluster
Switch to the monitoring cluster context:

```
kubectl config use-context monitoring-cluster
```

Create the monitoring namespace:

```
kubectl create namespace monitoring
```

Install Prometheus and Grafana using Helmfile:

```
helmfile -f helmfile-monitoring.yaml sync
```

Step 7: Install components on clusters one and two
Repeat these steps for both clusters:

Switch to the cluster context:

```
kubectl config use-context cluster-one
# or
kubectl config use-context cluster-two
```

Create the monitoring namespace:

```
kubectl create namespace monitoring
```

Install Node Exporter and Kube State Metrics:

```
helmfile -f helmfile-clusters.yaml sync
```

Step 8: Configure Prometheus to scrape metrics from other clusters
Edit the `prometheus-values.yaml` file to add remote scrape configs:

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
        - api_server: https://cluster-one-api-server:6443
          tls_config:
            ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
          bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
        - source_labels: [__meta_kubernetes_node_name]
          regex: (.+)
          target_label: __metrics_path__
          replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor

    - job_name: 'cluster-two-node-exporter'
      kubernetes_sd_configs:
        - api_server: https://cluster-two-api-server:6443
          tls_config:
            ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
          bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
        - source_labels: [__meta_kubernetes_node_name]
          regex: (.+)
          target_label: __metrics_path__
          replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
```

Update Prometheus on the monitoring cluster:

```
helmfile -f helmfile-monitoring.yaml sync
```

Step 9: Configure Grafana data sources
Access the Grafana UI (you may need to port-forward the Grafana service):

```
kubectl port-forward svc/grafana 3000:80 -n monitoring
```

Open a web browser and go to `http://localhost:3000`. Log in with the admin password you set in the `grafana-values.yaml` file.

Add Prometheus data sources:
1. Go to Configuration > Data Sources
2. Click "Add data source"
3. Select "Prometheus"
4. Set the name to "Monitoring Cluster"
5. Set the URL to `http://prometheus-server.monitoring.svc.cluster.local`
6. Click "Save & Test"

Repeat this process for the other two clusters, using their respective Prometheus URLs.

Step 10: Create Grafana dashboards
1. Go to "+" > Import
2. Enter dashboard ID 1860 (Node Exporter Full)
3. Select a Prometheus data source
4. Click "Import"

Repeat this process for other useful dashboards (e.g., 13105 for Kubernetes cluster monitoring).

To switch between clusters in your dashboards:
1. Edit the dashboard
2. Find the data source variable (usually named `DS_PROMETHEUS`)
3. Change the type to "Data source"
4. Set "Instance name filter" to `/Prometheus/`
5. Save the dashboard

Now you can select different clusters from the dashboard dropdown menu.

This setup allows you to monitor all three clusters from a central Grafana instance, with the ability to switch between clusters using dashboard variables. Remember to secure your clusters and consider using proper authentication and authorization mechanisms for production use.
