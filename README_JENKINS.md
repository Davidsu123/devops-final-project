# Jenkins CI Pipeline

## Overview

The Jenkins server is responsible for the **Continuous Integration (CI)** process in this project. It automates the application's testing and packaging workflow, which is automatically triggered by a `git push` to the GitLab repository.

---

## Architecture: Dynamic Kubernetes Agents

To ensure a clean and efficient build environment, Jenkins is configured to run dynamic build agents on top of Kubernetes.

* **Separate Pod per Build:** Each pipeline run provisions a new, temporary Pod that serves as the agent. This Pod is destroyed upon completion of the run.
* **Isolated Environment:** This approach guarantees that every build starts from scratch, with no dependencies or artifacts left over from previous builds.
* **Dedicated Containers:** The agent Pod contains separate containers for performing `python` and `docker` tasks.

---

## Pipeline Stages

The process is defined in the `Jenkinsfile` and is divided into the following stages:

1.  **Checkout:**
    * Pulls the most recent source code from the relevant branch in GitLab.

2.  **Unit Tests (Quality Gate):**
    * Installs dependencies from the `requirements.txt` file.
    * Runs automated tests using `pytest`. A failure in this stage will stop the entire pipeline.

3.  **Build & Push Docker Image:**
    * Builds a new Docker image based on the `Dockerfile`.
    * Tags the image with the build number and, for the `main` branch only, with the `latest` tag.
    * Pushes the new image to the Docker Hub registry.

---

## Installation and Configuration

* **Installation via Helm:** The Jenkins server is installed on the Kubernetes cluster using a Helm chart.
* **Centralized Configuration:** All server configurations, including the plugin list, resource allocation, and persistence settings, are managed in the `jenkins-values.yaml` file.
* **Pipeline as Code:** The pipeline's logic is fully defined in the `Jenkinsfile`, which is version-controlled alongside the application code.

---

## GitLab Integration (Workflow)

* **PIPE-01 (Feature Branch):** Any `push` to a development branch triggers the pipeline for validation purposes.
* **PIPE-02 (Main Branch):** Merging code into the `main` branch triggers the pipeline. A successful run results in a new `latest` version being pushed to Docker Hub, which signals to ArgoCD to begin the deployment process.