import pytest
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_token_returned_for_valid_credentials(anon_client, password):
    User.objects.create_user(username="alice", password=password)
    res = anon_client.post(
        "/api/token/", {"username": "alice", "password": password}, format="json"
    )
    assert res.status_code == 200
    assert "access" in res.data
    assert "refresh" in res.data


def test_token_rejected_for_wrong_password(anon_client, password):
    User.objects.create_user(username="alice", password=password)
    res = anon_client.post(
        "/api/token/", {"username": "alice", "password": "wrong"}, format="json"
    )
    assert res.status_code == 401


def test_token_rejected_for_unknown_user(anon_client):
    res = anon_client.post(
        "/api/token/", {"username": "nobody", "password": "whatever"}, format="json"
    )
    assert res.status_code == 401


def test_protected_endpoint_rejects_request_without_token(anon_client):
    res = anon_client.get("/jobs/job_list_api/")
    assert res.status_code in (401, 403)


def test_protected_endpoint_rejects_invalid_token(anon_client):
    anon_client.credentials(HTTP_AUTHORIZATION="Bearer not-a-real-token")
    res = anon_client.get("/jobs/job_list_api/")
    assert res.status_code in (401, 403)
