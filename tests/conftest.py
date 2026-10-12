import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from accounts.models import CandidateProfile, RecruiterProfile
from applications.models import Application
from jobs.models import Job

PASSWORD = "StrongPass123!"


def client_for(user):
    """Return an API client logged in with a real JWT from /api/token/."""
    client = APIClient()
    res = client.post(
        "/api/token/",
        {"username": user.username, "password": PASSWORD},
        format="json",
    )
    assert res.status_code == 200, res.content
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")
    return client


def make_candidate(username):
    user = User.objects.create_user(username=username, password=PASSWORD)
    return CandidateProfile.objects.create(user=user)


def make_recruiter(username):
    user = User.objects.create_user(username=username, password=PASSWORD)
    return RecruiterProfile.objects.create(user=user, company_name="Acme")


@pytest.fixture
def password():
    return PASSWORD


@pytest.fixture
def anon_client():
    return APIClient()


@pytest.fixture
def candidate(db):
    return make_candidate("candidate1")


@pytest.fixture
def candidate2(db):
    return make_candidate("candidate2")


@pytest.fixture
def recruiter(db):
    return make_recruiter("recruiter1")


@pytest.fixture
def recruiter2(db):
    return make_recruiter("recruiter2")


@pytest.fixture
def candidate_client(candidate):
    return client_for(candidate.user)


@pytest.fixture
def candidate2_client(candidate2):
    return client_for(candidate2.user)


@pytest.fixture
def recruiter_client(recruiter):
    return client_for(recruiter.user)


@pytest.fixture
def recruiter2_client(recruiter2):
    return client_for(recruiter2.user)


@pytest.fixture
def job(recruiter):
    return Job.objects.create(
        recruiter=recruiter,
        title="Django Developer",
        description="Build REST APIs",
        location="Chennai",
        salary=500000,
        skills="python,django",
    )


@pytest.fixture
def application(candidate, job):
    return Application.objects.create(candidate=candidate, job=job)
