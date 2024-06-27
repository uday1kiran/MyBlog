1. check the flannel configuration:

```
kubectl get cm -n kube-flannel kube-flannel-cfg -o yaml
```
Look the "Network" field in the config, likely set to "10.244.0.0/16" as default.

2. Check the PodCIDR assigned to your nodes.

```
kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}'
```
This is the network CIDR assigned when running kubeadm init.

3. If both not matching, update the Flannel configuration.
3.1 For that, delete the flannel deployment first.
```
kubectl delete -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```
3.2 Download the yaml file.
```
wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

3.3 Edit the yaml file and update the net-conf.json part to match the PodCIDR.

```yaml
net-conf.json:|
{
  "Network":"10.245.0.0/16"
  "Backend":{
  "Type":"vxlan"
 }
}
```

3.4 apply the updated configuration:
```
kubectl apply -f kube-flannel.yml
```

Wait for few minutes to check the status of pods and nodes.

```
kubectl get nodes
kubectl get pods -A
``` 

Note: AWS VPC CNI is often good choice for AWS environemnts.

```
kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/master/aws-k8s-cni.yaml
```
