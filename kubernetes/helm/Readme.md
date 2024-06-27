# Install helm
- [Reference link](https://helm.sh/docs/intro/install/)
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

# Install helmfile
- [Reference1](https://github.com/helmfile/helmfile/releases)
- [Reference2](https://helmfile.readthedocs.io/en/latest/)
```
wget https://github.com/helmfile/helmfile/releases/download/v0.165.0/helmfile_0.165.0_linux_amd64.tar.gz
mkdir temp
tar -xvzf helmfile_0.165.0_linux_amd64.tar.gz -C temp/
chmod +x temp/helmfile
sudo mv temp/helmfile /usr/local/bin/
rm -rf temp helmfile_0.165.0_linux_amd64.tar.gz
```

# Install kubectl
- [Reference](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-kubectl-binary-with-curl-on-linux)
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
##chmod +x kubectl
##sudo mv kubectl /usr/local/bin/
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```
