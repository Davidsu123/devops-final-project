# Argo CD (INF-03) and the dev environment (PIPE-03)

Argo CD deploys the app to the `dev` environment and keeps it up to date.

- Argo CD itself is installed with Helm, in the `argocd` namespace (as in the project schema).
- `application-dev.yaml` tells Argo CD what to deploy: the newest version of the Helm chart `final-project-chart` from Docker Hub, into the `dev` namespace.
- Every successful build of main pushes a new chart version (`1.0.<build number>`). Argo CD checks every few minutes, sees the new version and deploys it. Nobody runs a deploy command by hand.

## Install Argo CD

```
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm install argocd argo/argo-cd --version 10.11.6 -n argocd --create-namespace
```

Admin password (user `admin`):

```
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}"
```

The password comes out in base64. Decode it, then open the UI at https://localhost:8081:

```
kubectl -n argocd port-forward svc/argocd-server 8081:443
```

## Connect the app (dev environment)

The app in `dev` needs the database password too:

```
kubectl create namespace dev
kubectl -n dev create secret generic mongodb-secret --from-literal=MONGO_PASSWORD=<the-same-password>
kubectl apply -f infra/argocd/application-dev.yaml
```

The first version appears after the first successful build of main in Jenkins.
