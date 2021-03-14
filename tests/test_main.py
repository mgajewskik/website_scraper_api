import os

from tests.db.test_db import TestingSessionLocal


def test_post_website_invalid(db, client):

    response = client.post("/websites/", json={"url": "google.com"})

    assert response.status_code == 422
    assert response.json() == {"detail": "Provided URL is invalid."}


def test_post_website_valid(mocker, db, client, data_path, cleanup):

    mocker.patch("app.main.SessionLocal", TestingSessionLocal)

    response = client.post("/websites/", json={"url": "https://google.com"})
    data = response.json()

    assert response.status_code == 200
    assert data["url"] == "https://google.com"
    assert data["id"] == 1
    assert data["status"] == "pending"
    assert type(data["started_at"]) == str


def test_post_get_website_valid(mocker, db, client, data_path, cleanup):

    mocker.patch("app.main.SessionLocal", TestingSessionLocal)

    response = client.post("/websites/", json={"url": "https://google.com"})
    data = response.json()

    assert response.status_code == 200
    assert data["url"] == "https://google.com"
    assert data["id"] == 1
    assert data["status"] == "pending"
    assert type(data["started_at"]) == str

    response = client.get("/websites/1")
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "completed"
    assert type(data["started_at"]) == str
    assert type(data["completed_at"]) == str


def test_post_website_existing(db, client, data_path, cleanup):

    response = client.post("/websites/", json={"url": "https://google.com"})
    response = client.post("/websites/", json={"url": "https://google.com"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Website already processed/processing."}


def test_get_websites(db, client):

    response = client.get("/websites/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_website_existing(db, client, cleanup):

    response = client.post("/websites/", json={"url": "https://google.com"})
    response = client.get("/websites/1")
    data = response.json()

    assert response.status_code == 200
    assert data["url"] == "https://google.com"
    assert data["id"] == 1
    assert type(data["started_at"]) == str


def test_get_website_not_found(db, client):

    response = client.get("/websites/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Website not found."}


def test_download_website(db, client, cleanup):

    response = client.post("/websites/", json={"url": "https://google.com"})
    response = client.get("/websites/1/download/")
    header = response.headers

    assert response.status_code == 200
    assert header["content-type"] == "application/zip"


def test_download_website_not_found(db, client):

    response = client.get("/websites/1/download/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Website not found."}


def test_download_website_not_found(db, client, test_data_path):

    response = client.post("/websites/", json={"url": "https://google.com"})
    os.remove(os.path.join(test_data_path, "1.zip"))

    response = client.get("/websites/1/download/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Website resources not found."}
