[ Kube 1.1 ] Setup Kubernetes Cluster using Kubeadm on Ubuntu 20.04

https://www.youtube.com/watch?v=mMmxMoprxiY&list=PL34sAs7_26wNBRWM6BDhnonoA5FMERax0&index=3

https://github.com/justmeandopensource/kubernetes/blob/master/docs/install-cluster-ubuntu-20.md

https://www.youtube.com/watch?v=nfPf0pJ1YLI&list=PL34sAs7_26wNBRWM6BDhnonoA5FMERax0&index=159

kubenretes vagrant provisioning:
https://www.youtube.com/watch?v=AoEWX84h_ig&list=PL34sAs7_26wNBRWM6BDhnonoA5FMERax0&index=158

https://github.com/justmeandopensource/kubernetes/tree/master/vagrant-provisioning

vagrant up
scp root@172.16.16.100:/etc/kubernetes/admin.conf ~/.kube/config
kubectl cluster-info
kubectl get nodes -o wide
kubectl -n kube-system get all

on two different terminal below commands to check whether nodes got used and calico overlay network:
kubectl run --rm -it --image=alpine alipne -- sh
kubectl run --rm -it --image=alpine alipne2 -- sh
kubectl get pods -o wide

on container terminal, check:
hostname -i
ping <other container ip>


ssh root@172.16.16.101: --> one of worker node
ctr -h
ctr containers
ctr containers list
# will show empty as we didn't provide namespace

as containers created in namespaces in ctr.
ctr namespaces list
ctr --namespace k8s.io containers list
ctr containers info -h




docker playlist:
https://www.youtube.com/watch?v=MbenLNMMl-4&list=PL34sAs7_26wO2pVeB-2xdI76Tp8t704UN

learn kubernetes:
https://www.youtube.com/watch?v=YzaYqxW0wGs&list=PL34sAs7_26wNBRWM6BDhnonoA5FMERax0
  
  
## some more steps on installation
  
https://youtu.be/AoEWX84h_ig?list=PL34sAs7_26wODP4j6owN-36Vg-KbACgkT

gcl git@github.com:justmeandopensource/kubernetes
cd kubernetes/vagrant-provisioning

scp root@172.16.16.100:/etc/kubernetes/admin.conf ~/.kube/config
password:kubeadmin

kubectl cluster-info dump
kubectl get nodes
kubectl -n kube-system get all
kubectl get pods -o wide
kubectl run --rm -it --image=alpine alpine -- sh
#hostname -i

on the node of pod created:
ctr -h
ctr namespace/ns list
ctr containers/c list/ls --namespace <above_output>
ctr containers info <container_id>


istioctl:
https://youtu.be/WFu8OLXUETY?list=PL34sAs7_26wPkw9g-5NQPP_rHVzApGpKP

