
- docker and kind install on ubuntu 24.
  
[reference link for kubectl installation](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-kubectl-binary-with-curl-on-linux)
  
```
#!/bin/bash

              # Update packages
              sudo apt-get update

              # Install dependencies
              sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

              # Add Docker GPG key
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

              # Set up the Docker stable repository
              echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

              # Update packages again
              sudo apt-get update

              # Install Docker
              sudo apt-get install -y docker-ce docker-ce-cli containerd.io

              # Add the current user to the docker group
              sudo groupadd docker
              sudo usermod -aG docker $USER
              newgrp docker

              # Install Kind
              curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.15.0/kind-linux-amd64
              chmod +x ./kind
              sudo mv ./kind /usr/local/bin/kind

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
##chmod +x kubectl
##sudo mv kubectl /usr/local/bin/
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

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
run this command.
```
kind create cluster --name my-k8s --config kind-config.yml
```

- multi-node cluster with port mappings also.
```
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30000
    hostPort: 30000
    listenAddress: "0.0.0.0" # Optional, defaults to "0.0.0.0"
    protocol: tcp # Optional, defaults to tcp
  - containerPort: 31321
    hostPort: 31321
  - containerPort: 31300
    hostPort: 31300
- role: worker
- role: worker
```
