"""Unit tests (APP-03). They run in the CI pipeline without a real database:
mongomock is a MongoDB that lives in memory."""
import mongomock
import pytest
from pymongo.errors import ServerSelectionTimeoutError

import app as app_module
import db


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


@pytest.fixture
def working_db(monkeypatch):
    fake = mongomock.MongoClient()
    monkeypatch.setattr(db, "client", fake)
    monkeypatch.setattr(db, "visits", fake["finalproject"]["visits"])


# Every database call fails, like when MongoDB is down
@pytest.fixture
def broken_db(monkeypatch):
    def fail(*args, **kwargs):
        raise ServerSelectionTimeoutError("database is down")

    monkeypatch.setattr(db, "add_visit", fail)
    monkeypatch.setattr(db, "count_visits", fail)
    monkeypatch.setattr(db, "ping", fail)


# Feature: the database layer saves and counts visits
def test_db_saves_and_counts_visits(working_db):
    db.add_visit()
    db.add_visit()
    assert db.count_visits() == 2


# Feature: the web page shows the number of visits
def test_home_page_counts_visits(client, working_db):
    first = client.get("/")
    second = client.get("/")
    assert first.status_code == 200
    assert '<div class="count">1</div>' in first.get_data(as_text=True)
    assert '<div class="count">2</div>' in second.get_data(as_text=True)


# Feature: a clear error page when the database is down
def test_home_page_shows_error_when_database_is_down(client, broken_db):
    response = client.get("/")
    assert response.status_code == 503
    assert "The database is not available" in response.get_data(as_text=True)


# Feature: liveness check works even without the database
def test_health_works_even_when_database_is_down(client, broken_db):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "UP"


# Feature: readiness check follows the database
def test_ready_when_database_answers(client, working_db):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json()["status"] == "READY"


def test_not_ready_when_database_is_down(client, broken_db):
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.get_json()["status"] == "NOT READY"


# Feature: metrics for Prometheus
def test_metrics_page_has_visit_counter(client, working_db):
    client.get("/")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "app_page_visits_total" in response.get_data(as_text=True)
