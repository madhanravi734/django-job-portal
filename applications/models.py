from django.db import models
from accounts.models import CandidateProfile
from jobs.models import Job
# Create your models here.
class Application(models.Model):
    candidate=models.ForeignKey(CandidateProfile,on_delete=models.CASCADE)
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    applied_at=models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES =[("Pending", "Pending"),("Accepted", "Accepted"),("Rejected", "Rejected"),]
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default="Pending")

    class Meta:
        constraints = [models.UniqueConstraint(
                fields=["candidate", "job"],
                name="unique_candidate_job_application"
            )
        ]