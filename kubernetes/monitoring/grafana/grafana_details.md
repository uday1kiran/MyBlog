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

# I  created a serviceaccount but unable to retrieve token from it to use that on grafana running in different cluster.
If you're getting an empty output for the bearer token, it's possible that the service account secret hasn't been created yet or there might be an issue with the command syntax.

Here's an alternative approach to retrieve the bearer token for the Grafana service account:

1. First, get the name of the secret associated with the Grafana service account:

   ```
   kubectl get serviceaccount grafana -o jsonpath="{.secrets[0].name}"
   ```

   This command will output the name of the secret.

2. Then, use the secret name to retrieve the bearer token:

   ```
   kubectl get secret <secret-name> -o jsonpath="{.data.token}" | base64 --decode
   ```

   Replace `<secret-name>` with the actual name of the secret you obtained in the previous step.

   This command will decode the base64-encoded token and display it.

If the above steps still don't work or return an empty output, you can try the following:

1. Verify that the Grafana service account exists in the default namespace:

   ```
   kubectl get serviceaccount grafana -n default
   ```

   Make sure the service account is listed in the output.

2. Check if any secrets are associated with the Grafana service account:

   ```
   kubectl get serviceaccount grafana -n default -o yaml
   ```

   Look for the `secrets` field in the output and see if any secrets are listed.

3. If no secrets are associated with the service account, you can create a new secret manually:

   ```
   kubectl apply -f - <<EOF
   apiVersion: v1
   kind: Secret
   metadata:
     name: grafana-token
     annotations:
       kubernetes.io/service-account.name: grafana
   type: kubernetes.io/service-account-token
   EOF
   ```

   This will create a new secret named `grafana-token` associated with the Grafana service account.

4. Retrieve the bearer token using the newly created secret:

   ```
   kubectl get secret grafana-token -o jsonpath="{.data.token}" | base64 --decode
   ```

   This should display the bearer token.

If you still encounter issues or the output remains empty, double-check the namespace and service account names, and ensure that you have the necessary permissions to access the secrets.
