## Give me step by step instructions to spin up a node k3s cluster on 3 ubuntu vms running.
Here are the step-by-step instructions to set up a K3s cluster on 3 Ubuntu VMs:

1. Prepare the VMs:
   - Make sure you have 3 Ubuntu VMs running and accessible via SSH.
   - Update the system packages on each VM:
     ```
     sudo apt update && sudo apt upgrade -y
     ```

2. Install K3s on the first VM (master node):
   - SSH into the first VM.
   - Run the following command to install K3s and set it up as the master node:
     ```
     curl -sfL https://get.k3s.io | sh -
     ```
   - Once the installation is complete, retrieve the node token:
     ```
     sudo cat /var/lib/rancher/k3s/server/node-token
     ```
   - Copy the node token as it will be needed to join the worker nodes.

3. Install K3s on the worker nodes:
   - SSH into the second VM.
   - Run the following command to install K3s and join it as a worker node:
     ```
     curl -sfL https://get.k3s.io | K3S_URL=https://<master-node-ip>:6443 K3S_TOKEN=<node-token> sh -
     ```
     Replace `<master-node-ip>` with the IP address of the master node and `<node-token>` with the token you copied earlier.
   - Repeat the same step for the third VM.

4. Verify the cluster:
   - SSH back into the master node.
   - Run the following command to check the status of the nodes:
     ```
     sudo kubectl get nodes
     ```
   - You should see all three nodes listed with their status as "Ready".

5. Deploy a sample application (optional):
   - On the master node, create a sample deployment file named `sample.yaml`:
     ```yaml
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: sample-deployment
     spec:
       replicas: 3
       selector:
         matchLabels:
           app: sample-app
       template:
         metadata:
           labels:
             app: sample-app
         spec:
           containers:
           - name: sample-container
             image: nginx
             ports:
             - containerPort: 80
     ```
   - Apply the deployment:
     ```
     sudo kubectl apply -f sample.yaml
     ```
   - Verify the deployment:
     ```
     sudo kubectl get deployments
     ```
   - You should see the "sample-deployment" with 3 replicas.

6. Access the cluster:
   - You can now use `kubectl` on the master node to manage and interact with your K3s cluster.
   - To access the cluster from your local machine, you can copy the `kubeconfig` file from the master node:
     ```
     sudo cat /etc/rancher/k3s/k3s.yaml
     ```
   - Copy the contents of the file and save it on your local machine.
   - Update the `server` URL in the `kubeconfig` file to use the IP address of the master node instead of `localhost`.
   - Set the `KUBECONFIG` environment variable to point to the location of the `kubeconfig` file on your local machine.

That's it! You now have a K3s cluster running on 3 Ubuntu VMs. You can deploy and manage applications using Kubernetes commands and tools.

## Give a sample ingress, deployment and services step by step all files and commands
 Here's a step-by-step guide to create a sample ingress, deployment, and services, along with the necessary files and commands:

1. Create a deployment file:
   - Create a file named `deployment.yaml` with the following content:
     ```yaml
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: my-app
     spec:
       replicas: 3
       selector:
         matchLabels:
           app: my-app
       template:
         metadata:
           labels:
             app: my-app
         spec:
           containers:
           - name: my-app
             image: nginx
             ports:
             - containerPort: 80
     ```
   - Save the file.

2. Create a service file:
   - Create a file named `service.yaml` with the following content:
     ```yaml
     apiVersion: v1
     kind: Service
     metadata:
       name: my-app-service
     spec:
       selector:
         app: my-app
       ports:
       - port: 80
         targetPort: 80
     ```
   - Save the file.

3. Create an ingress file:
   - Create a file named `ingress.yaml` with the following content:
     ```yaml
     apiVersion: networking.k8s.io/v1
     kind: Ingress
     metadata:
       name: my-app-ingress
     spec:
       rules:
       - host: my-app.example.com
         http:
           paths:
           - path: /
             pathType: Prefix
             backend:
               service:
                 name: my-app-service
                 port:
                   number: 80
     ```
   - Save the file.

4. Apply the deployment:
   - Run the following command to apply the deployment:
     ```
     kubectl apply -f deployment.yaml
     ```
   - Verify the deployment:
     ```
     kubectl get deployments
     ```

5. Apply the service:
   - Run the following command to apply the service:
     ```
     kubectl apply -f service.yaml
     ```
   - Verify the service:
     ```
     kubectl get services
     ```

6. Apply the ingress:
   - Run the following command to apply the ingress:
     ```
     kubectl apply -f ingress.yaml
     ```
   - Verify the ingress:
     ```
     kubectl get ingress
     ```

7. Test the application:
   - Add an entry in your local machine's `/etc/hosts` file to map the hostname `my-app.example.com` to the IP address of your K3s cluster's ingress controller.
   - Open a web browser and visit `http://my-app.example.com`.
   - You should see the default Nginx welcome page, indicating that the application is accessible through the ingress.

That's it! You have now created a sample deployment, service, and ingress in your K3s cluster. The deployment runs three replicas of an Nginx container, the service exposes the deployment, and the ingress routes traffic to the service based on the specified hostname and path.

Remember to replace `my-app.example.com` with your desired hostname and ensure that your ingress controller is properly configured to handle ingress resources.

## Create a self signed certificate for my local domain testing purpose for trafeik ingress class

To create a self-signed certificate for your local domain for testing purposes with the Traefik Ingress controller, you can use the `openssl` command. Here's how you can do it:

1. Open a terminal or command prompt.

2. Run the following command to generate a private key:
   ```
   openssl genrsa -out localhost.key 2048
   ```
   This will generate a 2048-bit RSA private key and save it in a file named `localhost.key`.

3. Run the following command to generate a self-signed certificate:
   ```
   openssl req -new -x509 -key localhost.key -out localhost.crt -days 365 -subj /CN=localhost
   ```
   This command will create a new self-signed certificate using the private key generated in the previous step. The certificate will be valid for 365 days and have a Common Name (CN) of `localhost`. The certificate will be saved in a file named `localhost.crt`.

   Note: If you want to use a different domain name instead of `localhost`, replace `localhost` with your desired domain name in the `-subj /CN=localhost` part of the command.

4. You should now have two files: `localhost.key` (private key) and `localhost.crt` (self-signed certificate).

5. Create a Kubernetes Secret to store the certificate and private key:
   ```
   kubectl create secret tls local-tls --key localhost.key --cert localhost.crt
   ```
   This command creates a Secret named `local-tls` in the current namespace, which contains the private key and certificate.

6. Configure your Traefik Ingress resource to use the self-signed certificate. Here's an example:
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: example-ingress
     annotations:
       kubernetes.io/ingress.class: traefik
   spec:
     tls:
     - hosts:
       - localhost
       secretName: local-tls
     rules:
     - host: localhost
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: example-service
               port:
                 name: http
   ```
   In this example, the `tls` section specifies the `local-tls` Secret for the `localhost` host. Adjust the `host` and `paths` according to your requirements.

7. Apply the Ingress resource configuration:
   ```
   kubectl apply -f ingress.yaml
   ```
   Replace `ingress.yaml` with the actual filename of your Ingress resource configuration.

That's it! You have now created a self-signed certificate for your local domain and configured Traefik to use it for testing purposes. Keep in mind that self-signed certificates are not trusted by default and may trigger browser warnings when accessed. They are suitable for local development and testing environments but should not be used in production.

## More detailed: Enable ssl on this ingress url. And show me step by step process also. If above step didn't understand.

 Here's a step-by-step process to enable SSL on the ingress URL using Traefik as the ingress controller:

1. Obtain an SSL certificate:
   - You can either use a self-signed certificate for testing purposes or obtain a valid SSL certificate from a trusted certificate authority (CA) like Let's Encrypt.
   - For this example, we'll assume you have obtained a valid SSL certificate and have the certificate file (`cert.pem`) and private key file (`key.pem`) ready.

2. Create a secret to store the SSL certificate:
   - Run the following command to create a secret named `my-app-tls` with the SSL certificate and private key:
     ```
     kubectl create secret tls my-app-tls --cert=cert.pem --key=key.pem
     ```
   - Verify the secret:
     ```
     kubectl get secrets
     ```

3. Update the ingress file:
   - Modify the `ingress.yaml` file to enable SSL and use the created secret:
     ```yaml
     apiVersion: networking.k8s.io/v1
     kind: Ingress
     metadata:
       name: my-app-ingress
       annotations:
         kubernetes.io/ingress.class: traefik
         traefik.ingress.kubernetes.io/router.tls: "true"
     spec:
       tls:
       - hosts:
         - my-app.example.com
         secretName: my-app-tls
       rules:
       - host: my-app.example.com
         http:
           paths:
           - path: /
             pathType: Prefix
             backend:
               service:
                 name: my-app-service
                 port:
                   number: 80
     ```
   - Save the file.

4. Apply the updated ingress:
   - Run the following command to apply the updated ingress:
     ```
     kubectl apply -f ingress.yaml
     ```
   - Verify the ingress:
     ```
     kubectl get ingress
     ```

5. Configure Traefik to use the SSL certificate:
   - Ensure that Traefik is configured to use the SSL certificate for the specified hostname.
   - If you're using Traefik with its default configuration, it should automatically detect and use the SSL certificate stored in the secret.

6. Test the SSL connection:
   - Open a web browser and visit `https://my-app.example.com`.
   - Verify that the connection is secure and the SSL certificate is valid.

That's it! You have now enabled SSL on the ingress URL using Traefik. Traefik will automatically handle the SSL termination and route the traffic securely to your application.

Remember to replace `my-app.example.com` with your actual domain name and ensure that your DNS is properly configured to point to your K3s cluster's ingress controller.

Note: The specific steps may vary slightly depending on your Traefik version and configuration. Make sure to refer to the Traefik documentation for more details and advanced configuration options.



