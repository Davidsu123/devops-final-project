# Jenkins (INF-02)

Jenkins runs the CI pipelines of the app (PIPE-01 and PIPE-02).

- Installed with Helm, in the `default` namespace (as in the project schema).
- Every build runs in a temporary agent pod in the `default` namespace, and the pod is deleted when the build ends.
- Plugins: the list from the guidelines, in `values.yaml`. The prometheus plugin also exposes Jenkins metrics at `/prometheus` (bonus).

## Install

```
helm repo add jenkins https://charts.jenkins.io
helm repo update
helm install jenkins jenkins/jenkins --version 5.10.5 -f infra/jenkins/values.yaml
```

Admin password (user `admin`):

```
kubectl exec -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/additional/chart-admin-password
```

Open Jenkins at http://localhost:8080:

```
kubectl port-forward svc/jenkins 8080:8080
```

## Setup in the Jenkins UI

1. **Credentials** (Manage Jenkins > Credentials):
   - `dockerhub-credentials`: type "Username with password". Docker Hub user and an access token.
   - `discord-webhook`: type "Secret text". The webhook URL of a Discord channel (channel settings > Integrations > Webhooks).
2. **Email** (Manage Jenkins > System > E-mail Notification): SMTP server for the failure emails. For Gmail: `smtp.gmail.com`, SSL, port 465, and an app password.
3. **The job**: New Item > Multibranch Pipeline.
   - Branch Sources > Git > `https://github.com/Davidsu123/devops-final-project.git`
   - Scan Multibranch Pipeline Triggers > Periodically if not otherwise run > 1 minute

Jenkins checks GitHub every minute and runs the pipeline on every branch that changed. A Jenkins on a laptop cannot get webhooks from GitHub, so it checks by itself.

## What the pipeline does

One `Jenkinsfile` for all branches:

| Step | Feature branches (PIPE-01) | main (PIPE-02) |
|------|:---:|:---:|
| 1. Docker build of the image | yes | yes |
| 2. Unit tests (pytest) | yes | yes |
| 3. Helm lint + Helm template | yes | yes |
| 4. Helm package | | yes |
| 5. Docker push to Docker Hub | | yes |
| 6. Helm push to Docker Hub | | yes |
| 7. Discord message + email on failure | yes | yes |

An email is also sent when a failed build is fixed.

The image is built with Docker in Docker (dind): a Docker engine that runs inside the build pod. The build does not use the Docker of the server.
