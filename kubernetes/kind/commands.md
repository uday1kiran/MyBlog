- kind cluster commands.
```
kind get clusters ##to get list of clusters on machine
kind create cluster --name kind1 ##single node default settings.
kubectl get pods --context kind-kind1
kubectl cluster-info --context kind-kind1
kind delete cluster --name kind-3
```

- To expose ports from docker container of node of kind cluster
```
kind create cluster --name kind-3 --config=config.yaml
```
config.yaml
```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    listenAddress: "0.0.0.0" # Optional, defaults to "0.0.0.0"
    protocol: udp # Optional, defaults to tcp
  - containerPort: 30081
    hostPort: 30081
```

- In deployment of sample app.
```bash
cd eample-app
kubectl apply -f .
kubectl get deployments
kubectl get services
kubectl describe service example-service | grep NodePort
curl http://<IP_of_Node>:<NodePort> ##on host machine
```

- To create a multi-node cluster, below is the config file.
```
# three node (two workers) cluster config
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
```
