[Reference video: Install Promtail Loki Grafana on AWS EKS Demo](https://www.youtube.com/watch?v=5lYU3tonh1A
)

## For this testing purpose, I used kind cluster, goto kind folder for the reference:
```
kind create cluster --name kind-monitoring
kubectl config set-context kind-kind-monitoring
```

## Deployment steps
```
kubectl create ns loki
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install loki-stack grafana/loki-stack -n loki --set grafana.enabled=true

kubectl get pods -n loki -w
##to see the grafana url, user name is admin and password is:
kubectl get secret loki-stack-grafana -n loki -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

## to access the grafana service, I am exposing the service as nodePort and accessing that, be sure to use the port from extraPortMappings of kind.
export EDITOR=nano
kubectl edit svc loki-stack-grafana -n loki ##and update as nodePort with port value.
kubectl get svc -n loki
sudo ufw allow 30080/tcp
```

## To cleanup
```
helm uninstall loki-stack -n loki
kubectl delete ns loki
kind delete cluster --name kind-monitoring
```
