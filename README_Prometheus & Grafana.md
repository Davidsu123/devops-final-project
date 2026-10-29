Monitoring Stack: Prometheus & Grafana
1. OverviewThe project's monitoring stack provides real-time insights into the performance of the application and its underlying infrastructure. It is composed of two primary tools:Prometheus: A powerful system for collecting and storing time-series data, also known as metrics.Grafana: A leading platform for data visualization, allowing us to display the collected metrics in graphs and dashboards.2. Monitoring ArchitectureThe system operates on a "pull" model, where Prometheus proactively queries various services to collect data from them.

+-----------------+      Scrapes metrics     +----------------------+
|   Prometheus    | <-------------------- |   Our Application    |
|   (Scraper)     |      (every 30s)        | (Exposes /metrics)   |
+-----------------+                         +----------------------+
        |
        |  Stores data in its
        |  time-series database
        v
+-----------------+      Visualizes data     +----------------------+
|   Grafana       | --------------------> | Dashboards & Graphs  |
| (Visualizer)    |     (using PromQL)      |                      |
+-----------------+                         +----------------------+

Instrumentation: Our Flask application, thanks to the prometheus-flask-exporter library, exposes a /metrics endpoint. This endpoint presents a simple text-based view of all current metrics, such as flask_http_requests_total.Scraping: The Prometheus server is configured to automatically discover services in the cluster that have the correct annotations. Every few seconds, it sends a request to our application's /metrics endpoint, "scrapes" the data, and stores it in its database.Visualization: Grafana is connected to Prometheus as a data source. We build dashboards in Grafana, and each panel contains a query written in PromQL (Prometheus Query Language) to fetch and display the desired data from Prometheus.
3. Installation and ConfigurationInstallation via Helm: The entire monitoring stack is installed using the kube-prometheus-stack Helm chart. This package conveniently includes Prometheus, Grafana, and essential components like Alertmanager and ServiceMonitors, which simplify the scraping configuration process.Dedicated Namespace: All monitoring components are installed in a separate monitoring namespace to keep them isolated from other system components.
4. Example Metrics MonitoredHTTP Request Counter: Total number of requests served by the application.Request Latency: The average time it takes for the application to respond to requests.Status Codes: A breakdown of successful (200) versus failed (500) requests.Visit Counter: A custom metric that counts the total number of visits to the main page.