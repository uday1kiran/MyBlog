## For this demonstration purpose, I am using kind clusters. 
- How to install kind,helm,helmfile,kubectl: [First command set in this link](https://github.com/uday1kiran/MyBlog/blob/master/kubernetes/kind/commands.md)
- Create three clusters using kind, either multinode or single nodeby following the same link above.
- Here, I am using below commands two spin up clusters.

```
kind create cluster --name monitoring --config monitoring.yaml
kind create cluster --name cluster1 --config one.yaml
kind create cluster --name cluster2 --config two.yaml
```

extraPortMappings is used to expose nodePorts on the hostmachines.
  
monitoring.yaml
```
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    listenAddress: "0.0.0.0" # Optional, defaults to "0.0.0.0"
    protocol: udp # Optional, defaults to tcp
  - containerPort: 30080
    hostPort: 30080
```
one.yaml
```
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30081
    hostPort: 30081
```
two.yaml
```
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30082
    hostPort: 30082
```
- Once the clusters are up, next steps is to install prometheus on individual clusters.
- Based on the above extraPortMappings, using those port numbers to expose prometheus-server services on each clusters except monitoring(not required).

one\helmfile.yaml
``` 
repositories:
  - name: prometheus-community
    url: https://prometheus-community.github.io/helm-charts

releases:
  - name: prometheus
    namespace: monitoring
    chart: prometheus-community/prometheus
    version: 15.0.1
    values:
      - server:
          service:
            type: NodePort
            nodePort: 30081
```
two\helmfile.yaml
``` 
repositories:
  - name: prometheus-community
    url: https://prometheus-community.github.io/helm-charts

releases:
  - name: prometheus
    namespace: monitoring
    chart: prometheus-community/prometheus
    version: 15.0.1
    values:
      - server:
          service:
            type: NodePort
            nodePort: 30082
```

```
cd one
helmfile sync --kube-context kind-cluster1
cd ../two
helmfile sync --kube-context kind-cluster2
##check services of each cluster whether NodePort set or not
kubectl get svc prometheus-server -n monitoring --context kind-cluster1
kubectl get svc prometheus-server -n monitoring --context kind-cluster2
```

- Next step is to link above prometheus server to grafana in monitoring dashboard.
- helmfile.yaml for monitoring cluster, which should link other clusters also.
```
repositories:
       - name: prometheus-community
         url: https://prometheus-community.github.io/helm-charts
       - name: grafana
         url: https://grafana.github.io/helm-charts

releases:
       - name: prometheus
         chart: prometheus-community/prometheus
         namespace: monitoring
         values:
           - server:
               service:
                 type: NodePort

       - name: grafana
         chart: grafana/grafana
         namespace: monitoring
         values:
           - datasources:
               datasources.yaml:
                 apiVersion: 1
                 datasources:
                   - name: Prometheus
                     type: prometheus
                     url: http://prometheus-server.monitoring.svc.cluster.local
                     access: proxy
                     isDefault: true
                   {{- range $index, $clusterName := (list "cluster1" "cluster2") }}
                   - name: {{ $clusterName }}
                     type: prometheus
                     url: http://{{ index (list "10.11.53.16" "10.11.53.16") $index }}:{{ index (list 30081 30082) $index }}
                     access: proxy
                     isDefault: false
                   {{- end }}
```
- Or you can use below file, which will expose grafana only as NodePort and keep monitoring cluster prometheus-server as ClusterIP only.
```
#helmfile.yaml
repositories:
  - name: prometheus-community
    url: https://prometheus-community.github.io/helm-charts
  - name: grafana
    url: https://grafana.github.io/helm-charts

releases:
  - name: prometheus
    chart: prometheus-community/prometheus
    namespace: monitoring
    values:
      - server:
          service:
            type: ClusterIP

  - name: grafana
    chart: grafana/grafana
    namespace: monitoring
    values:
      - service:
          type: NodePort
          nodePort: 30080
      - datasources:
          datasources.yaml:
            apiVersion: 1
            datasources:
              - name: Prometheus
                type: prometheus
                url: http://prometheus-server.monitoring.svc.cluster.local
                access: proxy
                isDefault: true
              {{- range $index, $clusterName := (list "cluster1" "cluster2") }}
              - name: {{ $clusterName }}
                type: prometheus
                url: http://{{ index (list "10.11.53.16" "10.11.53.16") $index }}:{{ index (list 30081 30082) $index }}
                access: proxy
                isDefault: false
              {{- end }}
```

- commands used.
```
cd ../monitoring
helmfile sync --kube-context kind-monitoring
kubectl get svc grafana -n monitoring --context kind-monitoring
kubectl get secret --namespace monitoring grafana --context kind-monitoring -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
##username admin, password above output
```
- open browser and access http://<hostip>:<grafana_node_port> and see in the data sources section, entries will be added.
![image](https://github.com/uday1kiran/MyBlog/assets/9269442/adce1b3e-2550-49c0-895d-7e2550f2468e)
- And also you can import any dashboard from [dadshboards](https://github.com/uday1kiran/MyBlog/blob/k8s/kubernetes/monitoring/grafana_prometheus_import_dashboards.md) and can view these datasources under that.
![image](https://github.com/uday1kiran/MyBlog/assets/9269442/e2e56561-a160-4af1-a065-b56d6c0a7c91)

![image](https://github.com/uday1kiran/MyBlog/assets/9269442/b3cf8023-a952-4e06-8f00-236e96b04081)
