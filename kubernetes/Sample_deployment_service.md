Certainly! Here's an example of deploying an Nginx app using a Deployment and exposing it using a Service in Kubernetes:

1. Create a file named `nginx-deployment.yaml` with the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

This YAML file defines a Deployment named `nginx-deployment` that creates 3 replicas of an Nginx container. The container uses the `nginx:1.21` image and exposes port 80.

2. Create a file named `nginx-service.yaml` with the following content:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

This YAML file defines a Service named `nginx-service` that exposes the Nginx Deployment. The Service selects pods with the label `app: nginx` and maps port 80 of the Service to port 80 of the container. The Service type is set to `LoadBalancer`, which creates an external load balancer to access the Nginx app.

3. Apply the Deployment and Service using the following commands:

```bash
kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml
```

4. Verify that the Deployment and Service are created successfully:

```bash
kubectl get deployments
kubectl get services
```

You should see the `nginx-deployment` with 3 replicas and the `nginx-service` with an external IP address.

5. Access the Nginx app using the external IP address of the Service:

```bash
curl http://<external-ip>
```

Replace `<external-ip>` with the actual external IP address of the `nginx-service`.

That's it! You have successfully deployed an Nginx app using a Deployment and exposed it using a Service in Kubernetes. The Nginx app is now accessible via the external IP address of the Service.

Note: Make sure you have a Kubernetes cluster set up and configured before running these commands.
