# Prometheus and Grafana (INF-04)

Prometheus collects numbers from the app (visits, requests, errors, response time) and Grafana shows them as graphs.

- Installed with Helm (kube-prometheus-stack), in the `observation` namespace (as in the project schema).
- The app's Helm chart creates a ServiceMonitor. It tells Prometheus to read `/metrics` from the app every 15 seconds. Prometheus finds it by the label `release: prometheus`, which is why the release name below must be `prometheus`.

## Install

Install this before the app, because the app's chart creates a ServiceMonitor.

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --version 92.16.0 -n observation --create-namespace
```

## Grafana

Password (user `admin`):

```
kubectl -n observation get secret prometheus-grafana -o jsonpath="{.data.admin-password}"
```

The password comes out in base64. Decode it, then open Grafana at http://localhost:3000:

```
kubectl -n observation port-forward svc/prometheus-grafana 3000:80
```

## Metrics of the app

- `app_page_visits_total`: visits to the main page
- `flask_http_request_total`: requests by status code (200, 503 and so on)
- `flask_http_request_duration_seconds`: response time

Example query for a Grafana panel: `sum(rate(flask_http_request_total[5m])) by (status)`
