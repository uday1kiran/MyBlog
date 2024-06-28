create service account, secret, role and rolebindingusing yaml.
```
kubectl apply -f service_account.yaml
```
And the yaml file:
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-serviceaccount
---
apiVersion: v1
kind: Secret
metadata:
  name: my-serviceaccount-token
  annotations:
    kubernetes.io/service-account.name: my-serviceaccount
type: kubernetes.io/service-account-token
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: my-cluster-role
rules:
#- apiGroups: [""]
#  resources: ["nodes"]
#  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources:
  - nodes
  - nodes/proxy
  - services
  - endpoints
  - pods
  verbs: ["get", "list", "watch"]
- apiGroups:
  - extensions
  resources:
  - ingresses
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: my-cluster-rolebinding
subjects:
- kind: ServiceAccount
  name: my-serviceaccount
  namespace: default
roleRef:
  kind: ClusterRole
  name: my-cluster-role
  apiGroup: rbac.authorization.k8s.io
```

To retrieve the token after applying above yaml:
```
kubectl get secret my-serviceaccount-token -o jsonpath='{.data.token}' | base64 -d
```


To test the token
```
##TOKEN=$(kubectl get secret $(kubectl get sa my-serviceaccount -o jsonpath='{.secrets[0].name}') -o jsonpath='{.data.token}' | base64 --decode)
TOKEN=$(kubectl get secret my-serviceaccount-token -o jsonpath='{.data.token}' | base64 -d)
curl -H "Authorization: Bearer $TOKEN" https://<api-server-url>/api/v1/nodes
```

To test the token from a pod
```
kubectl run -it --rm test --image=curlimages/curl -- sh
## Inside the pod shell run below command.
curl -k https://10.11.53.51:6443/api/v1/nodes -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImdMVEZ6TEdjR05QcXBNMXZNN1VpSi1abVpaY052Q3V3TEdhQkZUbWFIRE0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6Im15LXNlcnZpY2VhY2NvdW50LXRva2VuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Im15LXNlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZDliOTU4MmItNDg5YS00NjliLWI4MTQtNDI2MjVmMmMwZDFhIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6bXktc2VydmljZWFjY291bnQifQ.xeE9sB8h6fPC0W_qVnNDxiCC0C7S15MK6Q3oZZA6qxP2A6MkaTO-XUvn-BW-JO6exy4KLLJDNSgfbWE9U16C638M6AY1bX8qKBQHUHBwiaVh7eE0TDF3Ct3I-xsNsQ3GuKNEZPiCHZ0w_TelOtE6HeSCT1f2KSYYq24r2FkOKbkIiUTqcMtEmho_UGmJn-Jpn7hwaoZlpAbXXQS0aaKN1_wDxuo5Q_gN97Yu54lFOeD4t58R44Y9c8ABb1S-EMdSJT-qX_vsYflKQIgK5sgmFyj8WBo_YGujiz6r4YzbeEcNnV_4lBkIf9eTffjPHPwmNHHnV49uB3reELt0frTLPQ"
```

To cleanup after work.
```
kubectl delete sa my-serviceaccount
```
