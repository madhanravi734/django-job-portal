import pytest

from jobs.models import Job

pytestmark = pytest.mark.django_db

LIST_URL = "/jobs/job_list_api/"


def detail_url(job_id):
    return f"/jobs/job_detail_api/{job_id}/"


def new_job_payload(**overrides):
    payload = {
        "title": "React Developer",
        "description": "Build UIs",
        "location": "Bangalore",
        "salary": 400000,
        "skills": "javascript,react",
    }
    payload.update(overrides)
    return payload


# ---------- listing ----------

def test_anonymous_user_cannot_list_jobs(anon_client, job):
    res = anon_client.get(LIST_URL)
    assert res.status_code in (401, 403)


def test_candidate_can_list_jobs(candidate_client, job):
    res = candidate_client.get(LIST_URL)
    assert res.status_code == 200
    assert res.data["count"] == 1
    assert res.data["results"][0]["title"] == "Django Developer"


def test_list_is_paginated(recruiter_client, recruiter):
    for i in range(30):
        Job.objects.create(
            recruiter=recruiter, title=f"Job {i}", description="d",
            location="Chennai", salary=i, skills="python",
        )
    res = recruiter_client.get(LIST_URL)
    assert res.status_code == 200
    assert res.data["count"] == 30
    assert res.data["next"] is not None
    assert len(res.data["results"]) < 30


def test_search_matches_title_and_skills(candidate_client, recruiter, job):
    Job.objects.create(
        recruiter=recruiter, title="React Developer", description="UIs",
        location="Bangalore", salary=1, skills="javascript",
    )
    res = candidate_client.get(LIST_URL, {"search": "django"})
    assert res.status_code == 200
    assert res.data["count"] == 1
    assert res.data["results"][0]["title"] == "Django Developer"

    res = candidate_client.get(LIST_URL, {"search": "javascript"})
    assert res.data["count"] == 1
    assert res.data["results"][0]["title"] == "React Developer"


def test_location_filter(candidate_client, recruiter, job):
    Job.objects.create(
        recruiter=recruiter, title="Other", description="d",
        location="Mumbai", salary=1, skills="x",
    )
    res = candidate_client.get(LIST_URL, {"location": "chennai"})
    assert res.data["count"] == 1
    assert res.data["results"][0]["location"] == "Chennai"


def test_ordering_by_salary(candidate_client, recruiter):
    for salary in (300, 100, 200):
        Job.objects.create(
            recruiter=recruiter, title=f"J{salary}", description="d",
            location="Chennai", salary=salary, skills="x",
        )
    asc = candidate_client.get(LIST_URL, {"ordering": "salary"})
    desc = candidate_client.get(LIST_URL, {"ordering": "-salary"})
    assert asc.data["results"][0]["salary"] == 100
    assert desc.data["results"][0]["salary"] == 300


# ---------- creating ----------

def test_recruiter_can_create_job_and_becomes_owner(recruiter_client, recruiter):
    res = recruiter_client.post(LIST_URL, new_job_payload(), format="json")
    assert res.status_code == 201
    job = Job.objects.get(title="React Developer")
    assert job.recruiter == recruiter


def test_candidate_cannot_create_job(candidate_client):
    res = candidate_client.post(LIST_URL, new_job_payload(), format="json")
    assert res.status_code == 403
    assert Job.objects.count() == 0


def test_create_job_with_missing_title_is_rejected(recruiter_client):
    payload = new_job_payload()
    del payload["title"]
    res = recruiter_client.post(LIST_URL, payload, format="json")
    assert res.status_code == 400
    assert Job.objects.count() == 0


# ---------- detail / ownership ----------

def test_any_logged_in_user_can_view_a_job(candidate_client, job):
    res = candidate_client.get(detail_url(job.id))
    assert res.status_code == 200
    assert res.data["title"] == "Django Developer"


def test_missing_job_returns_404(recruiter_client):
    res = recruiter_client.get(detail_url(99999))
    assert res.status_code == 404


def test_owner_can_update_job(recruiter_client, job):
    res = recruiter_client.patch(detail_url(job.id), {"salary": 600000}, format="json")
    assert res.status_code == 200
    job.refresh_from_db()
    assert job.salary == 600000


def test_other_recruiter_cannot_update_job(recruiter2_client, job):
    res = recruiter2_client.patch(detail_url(job.id), {"salary": 1}, format="json")
    assert res.status_code == 403
    job.refresh_from_db()
    assert job.salary == 500000


def test_candidate_cannot_update_job(candidate_client, job):
    res = candidate_client.patch(detail_url(job.id), {"salary": 1}, format="json")
    assert res.status_code == 403
    job.refresh_from_db()
    assert job.salary == 500000


def test_other_recruiter_cannot_delete_job(recruiter2_client, job):
    res = recruiter2_client.delete(detail_url(job.id))
    assert res.status_code == 403
    assert Job.objects.filter(id=job.id).exists()


def test_owner_can_delete_job(recruiter_client, job):
    res = recruiter_client.delete(detail_url(job.id))
    assert res.status_code == 204
    assert not Job.objects.filter(id=job.id).exists()


# ---------- validation rules ----------

def test_negative_salary_is_rejected_on_create(recruiter_client):
    res = recruiter_client.post(LIST_URL, new_job_payload(salary=-5), format="json")
    assert res.status_code == 400
    assert Job.objects.count() == 0


def test_blank_title_is_rejected_on_create(recruiter_client):
    res = recruiter_client.post(LIST_URL, new_job_payload(title="   "), format="json")
    assert res.status_code == 400
    assert Job.objects.count() == 0


def test_blank_title_is_rejected_on_partial_update(recruiter_client, job):
    res = recruiter_client.patch(detail_url(job.id), {"title": "   "}, format="json")
    assert res.status_code == 400
    job.refresh_from_db()
    assert job.title == "Django Developer"


def test_negative_salary_is_rejected_on_partial_update(recruiter_client, job):
    res = recruiter_client.patch(detail_url(job.id), {"salary": -1}, format="json")
    assert res.status_code == 400
    job.refresh_from_db()
    assert job.salary == 500000