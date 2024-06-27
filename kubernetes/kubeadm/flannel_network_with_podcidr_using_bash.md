Here's a script that automates the process of installing a Kubernetes cluster using kubeadm, setting up Flannel networking, and configuring the Pod CIDR in a single step:

If you have already installed kubeadm,helm,helmfile,kubectl using tools_install_steps.md and helm/Readme.md. Use below script.
```
#!/bin/bash

# Set variables
MASTER_IP="10.11.53.35"
POD_CIDR="10.244.0.0/16"  # Default Flannel Pod CIDR

# Initialize the Kubernetes cluster
sudo kubeadm init --pod-network-cidr=${POD_CIDR} --apiserver-advertise-address=${MASTER_IP}

# Set up kubeconfig for the current user
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

curl -o kube-flannel.yml https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

# Modify the Flannel manifest to use the custom CIDR
sed -i "s|10.244.0.0/16|${POD_CIDR}|g" kube-flannel.yml

# Apply the modified Flannel manifest
kubectl apply -f kube-flannel.yml

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
