import os
import socket

from flask import Flask, jsonify, render_template
from prometheus_client import Counter
from prometheus_flask_exporter import PrometheusMetrics
from pymongo.errors import PyMongoError

import db

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Custom metric: how many times the main page was opened
VISITS_COUNTER = Counter("app_page_visits_total", "Visits to the main page")

VERSION = os.environ.get("APP_VERSION", "dev")
POD_NAME = socket.gethostname()


@app.route("/")
def index():
    try:
        db.add_visit()
        count = db.count_visits()
    except PyMongoError:
        app.logger.exception("Could not reach the database")
        return render_template("index.html", count=None, pod_name=POD_NAME, version=VERSION), 503
    VISITS_COUNTER.inc()
    return render_template("index.html", count=count, pod_name=POD_NAME, version=VERSION)


# Liveness: is the app itself running? Does not check the database.
@app.route("/health")
def health():
    return jsonify(status="UP")


# Readiness: can the app reach the database?
@app.route("/ready")
def ready():
    try:
        db.ping()
    except PyMongoError:
        return jsonify(status="NOT READY"), 503
    return jsonify(status="READY")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
