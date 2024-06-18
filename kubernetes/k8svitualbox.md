o set up a local Kubernetes cluster on a VM and access it using a domain name set locally for ingress testing, you can follow these steps:

1. Set up a VM:
   - Choose a virtualization platform like VirtualBox or VMware.
   - Create a new VM with sufficient resources (e.g., 2 CPUs, 4GB RAM, 20GB disk).
   - Install a Linux distribution (e.g., Ubuntu) on the VM.

2. Install Kubernetes on the VM:
   - Update the package manager: `sudo apt update`
   - Install Docker: `sudo apt install docker.io`
   - Install Kubernetes components:
     ```
     sudo apt install apt-transport-https curl
     curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
     echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
     sudo apt update
     sudo apt install kubelet kubeadm kubectl
     ```
   - disable cgroup or else will get error during init.
      ```
      sed -i "s/cgroupDriver: systemd/cgroupDriver: cgroupfs/g" /var/lib/kubelet/config.yaml
      systemctl daemon-reload
      systemctl restart kubelet
      ```
   - Initialize the Kubernetes cluster: `sudo kubeadm init` or with custom ip: `sudo kubeadm init --apiserver-advertise-address=192.168.56.104 --pod-network-cidr=172.17.0.0/16`
   - Configure kubectl:
     ```
     mkdir -p $HOME/.kube
     sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
     sudo chown $(id -u):$(id -g) $HOME/.kube/config
     ```

3. Set up networking:
   - Install a pod network add-on like Calico or Flannel. For example, to install Calico:
     ```
     kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
     ```
3. Set up networking with Flannel:
   - Apply the Flannel manifest:
     ```
     kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
     ```
   - Wait for the Flannel pods to be running:
     ```
     kubectl get pods -n kube-system

4. Set up a local domain name:
   - Open the hosts file: `sudo nano /etc/hosts`
   - Add an entry mapping the desired domain name to the VM's IP address. For example:
     ```
     192.168.56.10 mydomain.local
     ```
   - Save and close the file.

5. Install and configure an Ingress controller:
   - Install the Nginx Ingress controller:
     ```
     kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.0/deploy/static/provider/baremetal/deploy.yaml
     ```
   - Wait for the Ingress controller pods to be running:
     ```
     kubectl get pods -n ingress-nginx
     ```

6. Create a test deployment and service:
   - Create a deployment YAML file (e.g., `test-deployment.yaml`):
     ```yaml
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: test-deployment
     spec:
       replicas: 2
       selector:
         matchLabels:
           app: test
       template:
         metadata:
           labels:
             app: test
         spec:
           containers:
           - name: test-container
             image: nginx
             ports:
             - containerPort: 80
     ```
   - Create a service YAML file (e.g., `test-service.yaml`):
     ```yaml
     apiVersion: v1
     kind: Service
     metadata:
       name: test-service
     spec:
       selector:
         app: test
       ports:
       - port: 80
         targetPort: 80
     ```
   - Apply the deployment and service:
     ```
     kubectl apply -f test-deployment.yaml
     kubectl apply -f test-service.yaml
     ```

7. Create an Ingress resource:
   - Create an Ingress YAML file (e.g., `test-ingress.yaml`):
     ```yaml
     apiVersion: networking.k8s.io/v1
     kind: Ingress
     metadata:
       name: test-ingress
       annotations:
         nginx.ingress.kubernetes.io/rewrite-target: /
     spec:
       rules:
       - host: mydomain.local
         http:
           paths:
           - path: /
             pathType: Prefix
             backend:
               service:
                 name: test-service
                 port:
                   number: 80
     ```
   - Apply the Ingress resource:
     ```
     kubectl apply -f test-ingress.yaml
     ```

8. Test the setup:
   - Open a web browser on your host machine.
   - Enter the domain name you set up (e.g., `http://mydomain.local`).
   - You should see the Nginx default page served by the test deployment.

That's it! You now have a local Kubernetes cluster set up on a VM, accessible using a locally defined domain name for ingress testing.

Note: Make sure to configure your host machine's network settings to allow communication with the VM, such as setting up port forwarding or using a bridged network adapter.
