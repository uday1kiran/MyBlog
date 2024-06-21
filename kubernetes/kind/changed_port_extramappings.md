 To modify the extra mappings for a Kind cluster without deleting it, you can follow these steps:

1. Open the Kind configuration file (`kind-config.yaml`) that you used to create the cluster. If you don't have the file, you can retrieve the current configuration by running the following command:

   ```
   kubectl get configmap -n kube-system kind-config -o jsonpath='{.data.config\.yaml}' > kind-config.yaml
   ```

2. Open the `kind-config.yaml` file in a text editor.

3. Locate the `extraPortMappings` section in the configuration file. It should look similar to this:

   ```yaml
   extraPortMappings:
     - containerPort: 3080
       hostPort: 3080
   ```

4. Change the `hostPort` value from `3080` to `30080`:

   ```yaml
   extraPortMappings:
     - containerPort: 3080
       hostPort: 30080
   ```

5. Save the changes to the `kind-config.yaml` file.

6. Apply the updated configuration to the existing Kind cluster by running the following command:

   ```
   kind update cluster --name <cluster-name> --config kind-config.yaml
   ```

   Replace `<cluster-name>` with the name of your Kind cluster.

7. Wait for the cluster to be updated with the new configuration. Kind will modify the existing cluster without deleting it.

After the update process is complete, your Kind cluster will have the updated extra port mapping, with the host port changed from `3080` to `30080`.

Please note that updating the extra port mapping may cause a brief interruption to the services running on that port, as Kind needs to reconfigure the cluster networking.
