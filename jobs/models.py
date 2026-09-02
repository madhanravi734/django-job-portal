from django.db import models
from accounts.models import RecruiterProfile
# Create your models here.
class Job(models.Model):
    recruiter=models.ForeignKey(RecruiterProfile,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.TextField()
    location=models.CharField(max_length=40)
    salary=models.IntegerField(default=0)
    skills = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
