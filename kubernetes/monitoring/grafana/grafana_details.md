# grafana password for the grafana running in kubernetes cluster. How to retrieve that?
To retrieve the Grafana password for a Grafana instance running in a Kubernetes cluster, you can follow these steps:

1. Check the Grafana deployment configuration:
   - If you deployed Grafana using a Helm chart or a Kubernetes manifest file, check the configuration files for any specified admin password.
   - Look for environment variables or secret references related to the Grafana password.

2. If the password is not specified in the configuration, Kubernetes might have automatically generated a random password for Grafana. In this case, you can retrieve the password from the Kubernetes secret associated with Grafana.

   Run the following command to list the secrets in the namespace where Grafana is deployed:
   ```
   kubectl get secrets -n <namespace>
   ```
   Replace `<namespace>` with the namespace where Grafana is running (e.g., `default` if not specified).

3. Look for a secret with a name related to Grafana, such as `grafana-admin-credentials` or similar.

4. Once you find the secret, you can retrieve the password by running:
   ```
   kubectl get secret <grafana-secret-name> -n <namespace> -o jsonpath="{.data.admin-password}" | base64 --decode
   ```
   Replace `<grafana-secret-name>` with the actual name of the Grafana secret and `<namespace>` with the namespace where Grafana is running.

   This command retrieves the `admin-password` key from the secret, decodes the base64-encoded value, and displays the plain-text password.

5. Use the retrieved password to log in to the Grafana web interface.

If the above steps don't work or you can't find the password, you can consider the following alternative approaches:

- Reset the Grafana admin password:
  - Access the Grafana CLI by executing into the Grafana pod:
    ```
    kubectl exec -it <grafana-pod-name> -n <namespace> -- /bin/bash
    ```
  - Run the password reset command:
    ```
    grafana-cli admin reset-admin-password <new-password>
    ```
  - Use the new password to log in to Grafana.

- Recreate the Grafana deployment with a known password:
  - Delete the existing Grafana deployment and associated resources.
  - Redeploy Grafana with a specified admin password in the configuration or using a Kubernetes secret.

Remember to follow security best practices and rotate the Grafana admin password regularly to ensure the security of your Grafana installation.

- Example: grafana deployed on a cluster using official helm chart.
```
kubectl get secrets -n monitoring --context kind-monitoring
NAME                               TYPE                 DATA   AGE
grafana                            Opaque               3      20m
sh.helm.release.v1.grafana.v1      helm.sh/release.v1   1      20m
sh.helm.release.v1.prometheus.v1   helm.sh/release.v1   1      20m

kubectl get secret grafana -n monitoring -o jsonpath="{.data.admin-password}" --context kind-monitoring | base64 --decode
dAnKdDVTS5cZo19zvT4cIT9L5EaVlsE11uCg63nA
```
