 I'll provide you with a detailed step-by-step guide on how to set up this multi-cluster monitoring setup using Kubernetes, Prometheus, and Grafana. This guide assumes you have basic knowledge of Kubernetes, Helm, and command-line tools.

Step 1: Set up the Kubernetes clusters

1. Create three Kubernetes clusters:
   - monitoring
   - cluster1
   - cluster2

   You can use tools like kubeadm, kops, or managed Kubernetes services like GKE, EKS, or AKS to create these clusters.

2. Configure kubectl to switch between clusters easily:

   ```
   kubectl config use-context monitoring
   kubectl config use-context cluster1
   kubectl config use-context cluster2
   ```

Step 2: Install Helm

Install Helm on your local machine if you haven't already:

```
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

Step 3: Set up monitoring cluster

1. Switch to the monitoring cluster:

   ```
   kubectl config use-context monitoring
   ```

2. Add the Prometheus and Grafana Helm repositories:

   ```
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo add grafana https://grafana.github.io/helm-charts
   helm repo update
   ```

3. Install Prometheus:

   ```
   helm install prometheus prometheus-community/prometheus
   ```

4. Install Grafana:

   ```
   helm install grafana grafana/grafana
   ```

5. Get the Grafana admin password:

   ```
   kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
   ```

6. Port-forward Grafana to access it locally:

   ```
   kubectl port-forward service/grafana 3000:80
   ```

   You can now access Grafana at http://localhost:3000

Step 4: Set up cluster1 and cluster2

Repeat these steps for both cluster1 and cluster2:

1. Switch to the cluster:

   ```
   kubectl config use-context cluster1  # or cluster2
   ```

2. Add the Prometheus Helm repository (if not already added):

   ```
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

3. Install Prometheus Node Exporter:

   ```
   helm install node-exporter prometheus-community/prometheus-node-exporter
   ```

4. Install Kube State Metrics:

   ```
   helm install kube-state-metrics prometheus-community/kube-state-metrics
   ```

Step 5: Configure Prometheus in the monitoring cluster to scrape metrics from cluster1 and cluster2

1. Switch back to the monitoring cluster:

   ```
   kubectl config use-context monitoring
   ```

2. Edit the Prometheus configuration to add scrape configs for cluster1 and cluster2:

   ```
   kubectl edit configmap prometheus-server
   ```

   Add the following scrape configs under the `scrape_configs` section:

   ```yaml
   - job_name: 'cluster1-node-exporter'
     kubernetes_sd_configs:
     - api_server: 'https://cluster1-api-server-url'
       role: node
       tls_config:
         insecure_skip_verify: true
     bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
     relabel_configs:
     - action: labelmap
       regex: __meta_kubernetes_node_label_(.+)
     - target_label: __address__
       replacement: cluster1-api-server-url:443
     - source_labels: [__meta_kubernetes_node_name]
       regex: (.+)
       target_label: __metrics_path__
       replacement: /api/v1/nodes/${1}:9100/proxy/metrics

   - job_name: 'cluster1-kube-state-metrics'
     kubernetes_sd_configs:
     - api_server: 'https://cluster1-api-server-url'
       role: pod
       tls_config:
         insecure_skip_verify: true
     bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
     relabel_configs:
     - action: labelmap
       regex: __meta_kubernetes_pod_label_(.+)
     - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_name]
       action: replace
       target_label: pod
       regex: (kube-state-metrics);(.+)
       replacement: ${2}
     - source_labels: [__meta_kubernetes_namespace]
       action: replace
       target_label: namespace
     - source_labels: [__meta_kubernetes_pod_name]
       action: replace
       target_label: pod
     - target_label: __address__
       replacement: cluster1-api-server-url:443
     - source_labels: [__meta_kubernetes_pod_name]
       regex: (.+)
       target_label: __metrics_path__
       replacement: /api/v1/namespaces/default/pods/${1}:8080/proxy/metrics

   # Repeat the above two job configurations for cluster2, replacing 'cluster1' with 'cluster2'
   ```

   Replace `cluster1-api-server-url` and `cluster2-api-server-url` with the actual API server URLs of your clusters.

3. Restart the Prometheus pod to apply the changes:

   ```
   kubectl delete pod -l app=prometheus,component=server
   ```

Step 6: Configure Grafana dashboard

1. Access Grafana at http://localhost:3000 (if you're still port-forwarding)

2. Add Prometheus as a data source:
   - Go to Configuration > Data Sources
   - Click "Add data source"
   - Select "Prometheus"
   - Set the URL to `http://prometheus-server`
   - Click "Save & Test"

3. Create a new dashboard:
   - Click the "+" icon in the left sidebar
   - Select "Create Dashboard"
   - Click "Add new panel"

4. Configure the panel:
   - In the query editor, select your Prometheus data source
   - Use a PromQL query to fetch metrics, e.g.:
     ```
     sum(node_cpu_seconds_total{mode="idle"}) by (cluster)
     ```
   - Add a variable to select the cluster:
     - Click the gear icon in the top right to open dashboard settings
     - Go to "Variables" and click "Add variable"
     - Name: cluster
     - Type: Query
     - Data source: Prometheus
     - Query: `label_values(node_cpu_seconds_total, cluster)`
     - Click "Apply"

   - Use the variable in your queries:
     ```
     sum(node_cpu_seconds_total{mode="idle", cluster="$cluster"})
     ```

5. Add more panels for different metrics, using the `$cluster` variable to filter data for the selected cluster.

6. Save the dashboard.

This setup allows you to monitor multiple Kubernetes clusters from a central Grafana dashboard. You can switch between clusters using the variable dropdown in the dashboard.

Remember to secure your clusters and consider using proper authentication and authorization methods for production environments. This guide provides a basic setup and may need to be adapted based on your specific requirements and security needs.

----

I'll provide you with steps to configure a comprehensive dashboard that shows metrics for multiple Kubernetes clusters and their nodes. We'll use Grafana's templating feature to switch between clusters easily.

Step 1: Prepare Grafana

1. Log in to Grafana (http://localhost:3000 if you're using port-forwarding).

2. Create a new dashboard:
   - Click the "+" icon in the left sidebar
   - Select "Create Dashboard"

Step 2: Set up Dashboard Variables

1. In the dashboard, click the gear icon in the top right to open dashboard settings.

2. Go to "Variables" and click "Add variable".

3. Set up a cluster variable:
   - Name: cluster
   - Type: Query
   - Data source: Prometheus
   - Query: `label_values(kube_node_info, cluster)`
   - Enable "Multi-value" and "Include All option"

4. Set up a node variable:
   - Name: node
   - Type: Query
   - Data source: Prometheus
   - Query: `label_values(kube_node_info{cluster="$cluster"}, node)`
   - Enable "Multi-value" and "Include All option"

5. Set up a namespace variable:
   - Name: namespace
   - Type: Query
   - Data source: Prometheus
   - Query: `label_values(kube_namespace_status_phase{cluster="$cluster"}, namespace)`
   - Enable "Multi-value" and "Include All option"

6. Click "Apply" to save the variables.

Step 3: Create Dashboard Panels

Now, let's create panels for various metrics. For each panel, click "Add panel" and configure as follows:

1. Cluster Overview:
   - Title: "Cluster Overview"
   - Visualization: Stat
   - Queries:
     a. `count(kube_node_info{cluster="$cluster"})`
     b. `sum(kube_pod_status_phase{cluster="$cluster", phase="Running"})`
     c. `sum(kube_namespace_status_phase{cluster="$cluster", phase="Active"})`

2. Node CPU Usage:
   - Title: "Node CPU Usage"
   - Visualization: Graph
   - Query: `100 - (avg by(instance) (irate(node_cpu_seconds_total{cluster="$cluster", mode="idle"}[5m])) * 100)`

3. Node Memory Usage:
   - Title: "Node Memory Usage"
   - Visualization: Graph
   - Query: `100 * (1 - ((avg_over_time(node_memory_MemFree_bytes{cluster="$cluster"}[5m]) + avg_over_time(node_memory_Cached_bytes{cluster="$cluster"}[5m]) + avg_over_time(node_memory_Buffers_bytes{cluster="$cluster"}[5m])) / avg_over_time(node_memory_MemTotal_bytes{cluster="$cluster"}[5m])))`

4. Node Disk Usage:
   - Title: "Node Disk Usage"
   - Visualization: Graph
   - Query: `100 - ((node_filesystem_avail_bytes{cluster="$cluster", mountpoint="/"} * 100) / node_filesystem_size_bytes{cluster="$cluster", mountpoint="/"})`

5. Pod Status:
   - Title: "Pod Status"
   - Visualization: Pie Chart
   - Query: `sum by (phase) (kube_pod_status_phase{cluster="$cluster"})`

6. Namespace Status:
   - Title: "Namespace Status"
   - Visualization: Pie Chart
   - Query: `sum by (phase) (kube_namespace_status_phase{cluster="$cluster"})`

7. Node Status:
   - Title: "Node Status"
   - Visualization: Table
   - Query: `kube_node_status_condition{cluster="$cluster", condition="Ready"}`

8. Pod Resource Requests and Limits:
   - Title: "Pod Resource Requests and Limits"
   - Visualization: Table
   - Queries:
     a. `sum by (namespace, pod) (kube_pod_container_resource_requests{cluster="$cluster", resource="cpu"}) * 1000`
     b. `sum by (namespace, pod) (kube_pod_container_resource_limits{cluster="$cluster", resource="cpu"}) * 1000`
     c. `sum by (namespace, pod) (kube_pod_container_resource_requests{cluster="$cluster", resource="memory"})`
     d. `sum by (namespace, pod) (kube_pod_container_resource_limits{cluster="$cluster", resource="memory"})`

9. Network I/O:
   - Title: "Network I/O"
   - Visualization: Graph
   - Queries:
     a. `sum(rate(node_network_receive_bytes_total{cluster="$cluster"}[5m]))`
     b. `sum(rate(node_network_transmit_bytes_total{cluster="$cluster"}[5m]))`

10. Container CPU Usage:
    - Title: "Container CPU Usage"
    - Visualization: Graph
    - Query: `sum by (pod_name) (rate(container_cpu_usage_seconds_total{cluster="$cluster", image!=""}[5m]))`

11. Container Memory Usage:
    - Title: "Container Memory Usage"
    - Visualization: Graph
    - Query: `sum by (pod_name) (container_memory_usage_bytes{cluster="$cluster", image!=""})`

Step 4: Organize the Dashboard

1. Arrange the panels in a logical order. For example:
   - Put the Cluster Overview at the top
   - Group node-related metrics together
   - Group pod and container metrics together

2. Adjust the time range selector at the top of the dashboard to allow users to view data for different time periods.

3. Add text panels to provide context or explanations where necessary.

Step 5: Set Dashboard Settings

1. Go to dashboard settings (gear icon in the top right)
2. In the "General" section:
   - Set a meaningful name for the dashboard
   - Add a description
   - Set refresh interval (e.g., every 1m)

3. In the "Variables" section, ensure your cluster, node, and namespace variables are set up correctly.

4. In the "Links" section, you can add links to other relevant dashboards or external resources.

Step 6: Save and Share

1. Save the dashboard.
2. To share the dashboard:
   - Click the share icon in the top navigation bar
   - You can get a direct link or embed code from here

This dashboard will provide a comprehensive view of your Kubernetes clusters, allowing you to switch between clusters using the variable at the top. You can further customize this dashboard by adding more specific metrics or panels based on your particular needs.

---
The sample prometheus config file to see the scrape settings.

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-server
  namespace: monitoring
  uid: 3320a228-6913-4acb-92aa-bb4b59a8e8b5
  resourceVersion: '5157'
  creationTimestamp: '2024-06-28T12:46:25Z'
  labels:
    app: prometheus
    app.kubernetes.io/managed-by: Helm
    chart: prometheus-15.10.1
    component: server
    heritage: Helm
    release: prometheus
  annotations:
    meta.helm.sh/release-name: prometheus
    meta.helm.sh/release-namespace: monitoring
  managedFields:
    - manager: helm
      operation: Update
      apiVersion: v1
      time: '2024-06-28T12:46:25Z'
      fieldsType: FieldsV1
      fieldsV1:
        f:data:
          .: {}
          f:alerting_rules.yml: {}
          f:alerts: {}
          f:allow-snippet-annotations: {}
          f:prometheus.yml: {}
          f:recording_rules.yml: {}
          f:rules: {}
        f:metadata:
          f:annotations:
            .: {}
            f:meta.helm.sh/release-name: {}
            f:meta.helm.sh/release-namespace: {}
          f:labels:
            .: {}
            f:app: {}
            f:app.kubernetes.io/managed-by: {}
            f:chart: {}
            f:component: {}
            f:heritage: {}
            f:release: {}
  selfLink: /api/v1/namespaces/monitoring/configmaps/prometheus-server
data:
  alerting_rules.yml: |
    {}
  alerts: |
    {}
  allow-snippet-annotations: 'false'
  prometheus.yml: |
    global:
      evaluation_interval: 15s
      scrape_interval: 15s
      scrape_timeout: 10s
    rule_files:
    - /etc/config/recording_rules.yml
    - /etc/config/alerting_rules.yml
    - /etc/config/rules
    - /etc/config/alerts
    scrape_configs:
    - job_name: 'kubernetes-metrics-server-cluster2'
      metrics_path: /metrics
      scheme: https
      static_configs:
        - targets: ['10.11.53.52:30443']
      tls_config:
        insecure_skip_verify: true
    - job_name: 'node-exporter-cluster2'
      static_configs:
        - targets: ['10.11.53.52:30910']
    - job_name: 'kube-state-metrics-cluster2'
      static_configs:
        - targets: ['10.11.53.52:30080']
    - job_name: prometheus
      static_configs:
      - targets:
        - localhost:9090
    - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      job_name: kubernetes-apiservers
      kubernetes_sd_configs:
      - role: endpoints
      relabel_configs:
      - action: keep
        regex: default;kubernetes;https
        source_labels:
        - __meta_kubernetes_namespace
        - __meta_kubernetes_service_name
        - __meta_kubernetes_endpoint_port_name
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        insecure_skip_verify: true
    - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      job_name: kubernetes-nodes
      kubernetes_sd_configs:
      - role: node
      relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - replacement: kubernetes.default.svc:443
        target_label: __address__
      - regex: (.+)
        replacement: /api/v1/nodes/$1/proxy/metrics
        source_labels:
        - __meta_kubernetes_node_name
        target_label: __metrics_path__
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        insecure_skip_verify: true
    - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      job_name: kubernetes-nodes-cadvisor
      kubernetes_sd_configs:
      - role: node
      relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - replacement: kubernetes.default.svc:443
        target_label: __address__
      - regex: (.+)
        replacement: /api/v1/nodes/$1/proxy/metrics/cadvisor
        source_labels:
        - __meta_kubernetes_node_name
        target_label: __metrics_path__
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        insecure_skip_verify: true
    - honor_labels: true
      job_name: kubernetes-service-endpoints
      kubernetes_sd_configs:
      - role: endpoints
      relabel_configs:
      - action: keep
        regex: true
        source_labels:
        - __meta_kubernetes_service_annotation_prometheus_io_scrape
      - action: drop
        regex: true
        source_labels:
        - __meta_kubernetes_service_annotation_prometheus_io_scrape_slow
      - action: replace
        regex: (https?)
        source_labels:
        - __meta_kubernetes_service_annotation_prometheus_io_scheme
        target_label: __scheme__
      - action: replace
        regex: (.+)
        source_labels:
        - __meta_kubernetes_service_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: (.+?)(?::\d+)?;(\d+)
        replacement: $1:$2
        source_labels:
        - __address__
        - __meta_kubernetes_service_annotation_prometheus_io_port
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_service_annotation_prometheus_io_param_(.+)
        replacement: __param_$1
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - action: replace
        source_labels:
        - __meta_kubernetes_namespace
        target_label: namespace
      - action: replace
        source_labels:
        - __meta_kubernetes_service_name
        target_label: service
      - action: replace
        source_labels:
        - __meta_kubernetes_pod_node_name
        target_label: node
    - honor_labels: true
      job_name: kubernetes-service-endpoints-slow
      kubernetes_sd_configs:
      - role: endpoints
      relabel_configs:
      - action: keep
        regex: true
        source_labels:
        - __meta_kubernetes_service_annotation_prometheus_io_scrape_slow
      - action: replace
        regex: (https?)
        source_labels:
        - __meta_kubernetes_service_annotation_prometheus_io_scheme
        target_label: __scheme__
      - action: replace
        regex: (.+)
        source_labels:
        - __meta_kubernetes_service_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: (.+?)(?::\d+)?;(\d+)
        replacement: $1:$2
        source_labels:
        - __address__
        - __meta_kubernetes_service_annotation_prometheus_io_port
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_service_annotation_prometheus_io_param_(.+)
        replacement: __param_$1
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - action: replace
        source_labels:
        - __meta_kubernetes_namespace
        target_label: namespace
      - action: replace
        source_labels:
        - __meta_kubernetes_service_name
        target_label: service
      - action: replace
        source_labels:
        - __meta_kubernetes_pod_node_name
        target_label: node
      scrape_interval: 5m
      scrape_timeout: 30s
    - honor_labels: true
      job_name: prometheus-pushgateway
      kubernetes_sd_configs:
      - role: service
      relabel_configs:
      - action: keep
        regex: pushgateway
        source_labels:
        - __meta_kubernetes_service_annotation_prometheus_io_probe
    - honor_labels: true
      job_name: kubernetes-services
      kubernetes_sd_configs:
      - role: service
      metrics_path: /probe
      params:
        module:
        - http_2xx
      relabel_configs:
      - action: keep
        regex: true
        source_labels:
        - __meta_kubernetes_service_annotation_prometheus_io_probe
      - source_labels:
        - __address__
        target_label: __param_target
      - replacement: blackbox
        target_label: __address__
      - source_labels:
        - __param_target
        target_label: instance
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - source_labels:
        - __meta_kubernetes_namespace
        target_label: namespace
      - source_labels:
        - __meta_kubernetes_service_name
        target_label: service
    - honor_labels: true
      job_name: kubernetes-pods
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - action: keep
        regex: true
        source_labels:
        - __meta_kubernetes_pod_annotation_prometheus_io_scrape
      - action: drop
        regex: true
        source_labels:
        - __meta_kubernetes_pod_annotation_prometheus_io_scrape_slow
      - action: replace
        regex: (https?)
        source_labels:
        - __meta_kubernetes_pod_annotation_prometheus_io_scheme
        target_label: __scheme__
      - action: replace
        regex: (.+)
        source_labels:
        - __meta_kubernetes_pod_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: (.+?)(?::\d+)?;(\d+)
        replacement: $1:$2
        source_labels:
        - __address__
        - __meta_kubernetes_pod_annotation_prometheus_io_port
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_annotation_prometheus_io_param_(.+)
        replacement: __param_$1
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - action: replace
        source_labels:
        - __meta_kubernetes_namespace
        target_label: namespace
      - action: replace
        source_labels:
        - __meta_kubernetes_pod_name
        target_label: pod
      - action: drop
        regex: Pending|Succeeded|Failed|Completed
        source_labels:
        - __meta_kubernetes_pod_phase
    - honor_labels: true
      job_name: kubernetes-pods-slow
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - action: keep
        regex: true
        source_labels:
        - __meta_kubernetes_pod_annotation_prometheus_io_scrape_slow
      - action: replace
        regex: (https?)
        source_labels:
        - __meta_kubernetes_pod_annotation_prometheus_io_scheme
        target_label: __scheme__
      - action: replace
        regex: (.+)
        source_labels:
        - __meta_kubernetes_pod_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: (.+?)(?::\d+)?;(\d+)
        replacement: $1:$2
        source_labels:
        - __address__
        - __meta_kubernetes_pod_annotation_prometheus_io_port
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_annotation_prometheus_io_param_(.+)
        replacement: __param_$1
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - action: replace
        source_labels:
        - __meta_kubernetes_namespace
        target_label: namespace
      - action: replace
        source_labels:
        - __meta_kubernetes_pod_name
        target_label: pod
      - action: drop
        regex: Pending|Succeeded|Failed|Completed
        source_labels:
        - __meta_kubernetes_pod_phase
      scrape_interval: 5m
      scrape_timeout: 30s
  recording_rules.yml: |
    {}
  rules: |
    {}
binaryData: {}
fcl

```

