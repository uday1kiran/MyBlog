```
helm install elasticsearch elastic/elasticsearch -f elasticsearch-values.yaml
```

And the elasticsearch-values.yaml, for testing purpose it is created without Persistent storage volumes and NodePort enabled.
```
replicas: 2
minimumMasterNodes: 1
esJavaOpts: "-Xmx512m -Xms512m"
resources:
  requests:
    cpu: "100m"
    memory: "1Gi"
  limits:
    cpu: "1000m"
    memory: "2Gi"
service:
  type: NodePort

# Disable persistence
persistence:
  enabled: false

# Use emptyDir instead
volumeClaimTemplate:
  accessModes: [ "ReadWriteOnce" ]
  resources:
    requests:
      storage: 1Gi

# Disable antiAffinity for single-node setups
antiAffinity: "soft"

# Disable sysctlInitContainer for local testing
sysctlInitContainer:
  enabled: false
```

To get password of elastic user:
```
##username: elastic
kubectl get secrets --namespace=default elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d
```

And the service is elasticserach-master with nodeport of 9200: https://10.11.53.37:32133/
```
kubectl get svc
NAME                            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE
elasticsearch-master            NodePort    10.103.176.241   <none>        9200:32133/TCP,9300:31550/TCP   6m50s
elasticsearch-master-headless   ClusterIP   None             <none>        9200/TCP,9300/TCP               6m50s
kubernetes                      ClusterIP   10.96.0.1        <none>        443/TCP                         123m
```

