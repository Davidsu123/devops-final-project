# Sela Final Project: End-to-End CI/CD Web Application

This project demonstrates a complete, end-to-end CI/CD pipeline for a database-backed web application, built on modern DevOps principles and tools.

## Project Overview

The goal of this project is to build, test, deploy, and monitor a Python Flask application automatically. Every code change pushed to the Git repository triggers a CI pipeline that runs automated tests, builds a new Docker image, and pushes it to a container registry. A GitOps controller (ArgoCD) then detects the new version and automatically deploys it to a Kubernetes cluster. The entire system is monitored using Prometheus and Grafana.

---

## Workflow Diagram

This diagram shows the automated flow from a code push to a live deployment:

(GitLab)           (Jenkins)              (Docker Hub)           (ArgoCD)            (Kubernetes)
Git Push    -->    CI Pipeline Runs    -->   New Image Push   -->   Detects Change   -->   Rolls out New Version
(Code)             (Test & Build)           (Registry)             (Syncs State)          (Live App)


---

## Technology Stack

* **Version Control:** GitLab
* **Application:** Python, Flask
* **Database:** MongoDB
* **Testing:** Pytest
* **Containerization:** Docker, Docker Hub
* **CI (Continuous Integration):** Jenkins
* **CD (Continuous Deployment):** ArgoCD
* **Deployment:** Helm
* **Orchestration:** Kubernetes (running on Docker Desktop)
* **Monitoring:** Prometheus & Grafana

---

## Key Features

* **Automated CI Pipeline:** Every `git push` automatically triggers a Jenkins pipeline to validate the code.
* **Pipeline-as-Code:** The entire CI process is defined declaratively in the `Jenkinsfile`, allowing for version control of the pipeline itself.
* **Dynamic Build Agents:** Jenkins uses the Kubernetes plugin to spin up temporary, clean build environments for each run, ensuring no interference between jobs.
* **Automated Quality Gates:** The pipeline includes a dedicated stage to run `pytest` unit tests, preventing bugs from proceeding to the next stage.
* **GitOps Deployment:** ArgoCD monitors the Git repository and automatically syncs the application state in Kubernetes to match the desired state defined in the Helm chart.
* **Database Integration:** The application connects to a MongoDB instance running within the cluster to provide data persistence.
* **Built-in Monitoring:** The application is instrumented to expose performance metrics, which are automatically collected by Prometheus and can be visualized in Grafana.

---

## How to Run

1.  **Prerequisites:**
    * Docker Desktop with Kubernetes enabled.
    * Helm CLI installed.
    * `kubectl` configured to point to the Docker Desktop cluster.

2.  **Clone the Repository:**
    ```bash
    git clone [https://gitlab.com/sela-tracks/1116/students/david/final-project-app.git](https://gitlab.com/sela-tracks/1116/students/david/final-project-app.git)
    cd final-project-app
    ```
   

### 3. Setup & Deployment:

**IMPORTANT: Before deploying, you must create the MongoDB secret in your cluster. Run the following command, replacing 'your-password' with your actual password:**

kubectl create secret generic mongodb-secret --from-literal=MONGO_PASSWORD='your-super-secret-password'
```markdown
* It's recommended to use the "Fresh Start" script which resets the Kubernetes cluster and installs Jenkins and ArgoCD.
* After installation, configure the necessary credentials and webhooks in Jenkins and GitLab.
* ArgoCD will then automatically discover and deploy the application from the `chart/` directory in this repository.

4.  **Accessing Services:**
    * **Application:** Exposed via a `NodePort` on the Kubernetes cluster.
    * **Jenkins/ArgoCD/Grafana:** Accessible via `kubectl port-forward`.

---

This project was completed as part of the Sela DevOps course.

amir