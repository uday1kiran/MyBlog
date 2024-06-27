Here's a script that automates the process of installing a Kubernetes cluster using kubeadm, setting up Flannel networking with Helm, and configuring the Pod CIDR in a single step:

```bash
#!/bin/bash

# Set variables
MASTER_IP="<your-master-ip>"
POD_CIDR="10.244.0.0/16"  # Default Flannel Pod CIDR
KUBERNETES_VERSION="1.23.0"  # Specify your desired Kubernetes version

# Install dependencies
sudo apt-get update
sudo apt-get install -y docker.io apt-transport-https curl

# Add Kubernetes repo and install kubeadm, kubelet, and kubectl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubeadm=${KUBERNETES_VERSION}-00 kubelet=${KUBERNETES_VERSION}-00 kubectl=${KUBERNETES_VERSION}-00
sudo apt-mark hold kubeadm kubelet kubectl

# Initialize the Kubernetes cluster
sudo kubeadm init --pod-network-cidr=${POD_CIDR} --apiserver-advertise-address=${MASTER_IP}

# Set up kubeconfig for the current user
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

# Add Flannel Helm repo
helm repo add flannel https://flannel-io.github.io/helm-charts/

# Install Flannel using Helm
helm install flannel flannel/flannel --namespace kube-system --set podCidr="${POD_CIDR}"

# Remove the taint on the master node to allow pod scheduling
kubectl taint nodes --all node-role.kubernetes.io/master-

echo "Kubernetes cluster setup complete!"
echo "You can now join worker nodes using the kubeadm join command provided above."
```

Before running this script, make sure to:

1. Replace `<your-master-ip>` with the actual IP address of your master node.
2. Adjust the `POD_CIDR` if you want to use a different CIDR range for your pods.
3. Modify the `KUBERNETES_VERSION` if you want to install a different version of Kubernetes.

To use this script:

1. Save it to a file (e.g., `setup_kubernetes.sh`).
2. Make it executable: `chmod +x setup_kubernetes.sh`
3. Run it with sudo privileges: `sudo ./setup_kubernetes.sh`

This script will:

- Install necessary dependencies
- Set up the Kubernetes repository
- Install kubeadm, kubelet, and kubectl
- Initialize the Kubernetes cluster with the specified Pod CIDR
- Set up the kubeconfig file
- Install Helm
- Use Helm to install Flannel networking
- Remove the master node taint to allow pod scheduling on the master (useful for single-node clusters)

After running this script, you'll have a functioning Kubernetes cluster with Flannel networking set up. The script will output the `kubeadm join` command that you can use to add worker nodes to your cluster.

Note: This script is designed for Ubuntu/Debian-based systems. If you're using a different OS, you may need to modify the package installation commands accordingly.
