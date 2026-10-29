import os
import datetime
from flask import Flask, jsonify
from pymongo import MongoClient, errors
from prometheus_flask_exporter import PrometheusMetrics

# Initialize the Flask application and metrics exporter
app = Flask(__name__)
metrics = PrometheusMetrics(app)

# --- DATABASE CONNECTION ---
# Get password from environment variable for security
MONGODB_PASSWORD = os.environ.get("MONGO_PASSWORD")

if not MONGODB_PASSWORD:
    raise ValueError("MONGO_PASSWORD environment variable not set")

# Connect to MongoDB using the internal Kubernetes service name ('mongodb')
client = MongoClient(f"mongodb://root:{MONGODB_PASSWORD}@mongodb.default.svc.cluster.local:27017/")
db = client.finalproject
visits_collection = db.visits


@app.route('/')
def index():
    """Increments visit counter and returns the total number of visits."""
    try:
        visits_collection.insert_one({"visit_time": datetime.datetime.utcnow()})
        count = visits_collection.count_documents({})
        return jsonify(message=f"Successfully connected to MongoDB! Page visits: {count}.")
    except Exception as e:
        return jsonify(message="Error connecting to the database.", error=str(e)), 500


@app.route('/health')
def health_check():
    """Health check endpoint for Kubernetes probes."""
    try:
        # Check the database connection by pinging the admin database
        client.admin.command('ping')
        return jsonify(status="UP", db_connection="OK"), 200
    except Exception as e:
        return jsonify(status="DOWN", error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
