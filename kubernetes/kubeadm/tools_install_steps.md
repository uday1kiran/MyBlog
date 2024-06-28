Reference: [Step by step instructions to install kubeadm and install calico network and deploy a sample nginx app](https://www.linuxtechi.com/install-kubernetes-on-ubuntu-24-04/#google_vignette)

```bash
sudo apt-get -y update
sudo apt-get install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
sudo modprobe overlay
sudo modprobe br_netfilter
sudo tee /etc/modules-load.d/k8s.conf <<EOF
overlay
br_netfilter
EOF
sudo tee /etc/sysctl.d/kubernetes.conf <<EOT
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOT
sudo sysctl --system
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --yes --dearmour -o /etc/apt/trusted.gpg.d/containerd.gpg
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" -y
sudo apt update && sudo apt install containerd.io -y
containerd config default | sudo tee /etc/containerd/config.toml >/dev/null 2>&1
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
sudo systemctl restart containerd
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --yes --dearmor -o /etc/apt/keyrings/k8s.gpg
echo 'deb [signed-by=/etc/apt/keyrings/k8s.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | sudo tee /etc/apt/sources.list.d/k8s.list
sudo apt update -y
sudo apt install kubelet kubeadm kubectl -y
```

- Create a cluster
```
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

- For calico network
```
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml
```
- Flannel network
```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

- flannel got from documentation, latest one [reference](https://github.com/flannel-io/flannel#deploying-flannel-manually)
```
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```

- If you want to change the podcidr of flannel network or having issues with the network deployed, check the flannel-network-cidr-change.md


- Optional: If you want to a node worker label.
```
vmadmin@kubeadm3:~$ kubectl get nodes
NAME       STATUS   ROLES           AGE     VERSION
kubeadm3   Ready    control-plane   3m40s   v1.30.2
kubeadm4   Ready    <none>          39s     v1.30.2
vmadmin@kubeadm3:~$ kubectl label node kubeadm4 node-role.kubernetes.io/worker=worker
node/kubeadm4 labeled
```
