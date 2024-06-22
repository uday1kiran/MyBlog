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
rm -rf temp
```
