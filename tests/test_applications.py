import pytest
from django.db import IntegrityError, transaction

from applications.models import Application

pytestmark = pytest.mark.django_db


def apply_url(job_id):
    return f"/applications/apply_job_api/{job_id}/"


def detail_url(application_id):
    return f"/applications/application_detail_api/{application_id}/"


LIST_URL = "/applications/application_list_api/"


# ---------- applying ----------

def test_candidate_can_apply_to_a_job(candidate_client, candidate, job):
    res = candidate_client.post(apply_url(job.id))
    assert res.status_code == 201
    application = Application.objects.get()
    assert application.candidate == candidate
    assert application.job == job
    assert application.status == "Pending"


def test_candidate_cannot_apply_twice_to_the_same_job(candidate_client, job):
    first = candidate_client.post(apply_url(job.id))
    second = candidate_client.post(apply_url(job.id))
    assert first.status_code == 201
    assert second.status_code == 400
    assert Application.objects.count() == 1


def test_database_blocks_duplicate_application(candidate, job):
    Application.objects.create(candidate=candidate, job=job)
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Application.objects.create(candidate=candidate, job=job)
    assert Application.objects.count() == 1


def test_recruiter_cannot_apply_to_a_job(recruiter_client, job):
    res = recruiter_client.post(apply_url(job.id))
    assert res.status_code == 403
    assert Application.objects.count() == 0


def test_anonymous_user_cannot_apply(anon_client, job):
    res = anon_client.post(apply_url(job.id))
    assert res.status_code == 401
    assert Application.objects.count() == 0


def test_applying_to_missing_job_returns_404(candidate_client):
    res = candidate_client.post(apply_url(99999))
    assert res.status_code == 404


# ---------- listing ----------

def test_candidate_sees_only_their_own_applications(
    candidate_client, candidate2_client, application
):
    mine = candidate_client.get(LIST_URL)
    theirs = candidate2_client.get(LIST_URL)
    assert mine.status_code == 200
    assert len(mine.data) == 1
    assert len(theirs.data) == 0


def test_recruiter_sees_applications_only_for_their_own_jobs(
    recruiter_client, recruiter2_client, application
):
    owner = recruiter_client.get(LIST_URL)
    other = recruiter2_client.get(LIST_URL)
    assert len(owner.data) == 1
    assert len(other.data) == 0


# ---------- detail ----------

def test_candidate_and_job_recruiter_can_view_an_application(
    candidate_client, recruiter_client, application
):
    assert candidate_client.get(detail_url(application.id)).status_code == 200
    assert recruiter_client.get(detail_url(application.id)).status_code == 200


def test_unrelated_users_cannot_view_an_application(
    candidate2_client, recruiter2_client, application
):
    assert candidate2_client.get(detail_url(application.id)).status_code == 403
    assert recruiter2_client.get(detail_url(application.id)).status_code == 403


def test_missing_application_returns_404(recruiter_client):
    res = recruiter_client.get(detail_url(99999))
    assert res.status_code == 404


# ---------- status changes ----------

def test_job_owner_can_accept_an_application(recruiter_client, application):
    res = recruiter_client.patch(
        detail_url(application.id), {"status": "Accepted"}, format="json"
    )
    assert res.status_code == 200
    application.refresh_from_db()
    assert application.status == "Accepted"


def test_candidate_cannot_change_their_own_application_status(
    candidate_client, application
):
    res = candidate_client.patch(
        detail_url(application.id), {"status": "Accepted"}, format="json"
    )
    assert res.status_code == 403
    application.refresh_from_db()
    assert application.status == "Pending"


def test_other_recruiter_cannot_change_application_status(
    recruiter2_client, application
):
    res = recruiter2_client.patch(
        detail_url(application.id), {"status": "Accepted"}, format="json"
    )
    assert res.status_code == 403
    application.refresh_from_db()
    assert application.status == "Pending"
