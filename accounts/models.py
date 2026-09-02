from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class CandidateProfile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      phone = models.CharField(max_length=15)
      skills = models.CharField(max_length=300)
      education = models.CharField(max_length=200)
      experience = models.IntegerField(default=0)
      resume = models.FileField(upload_to="")

class RecruiterProfile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      company_name =models.CharField(max_length=50)
      company_description = models.TextField()
      company_website=models.URLField(max_length=200,blank=True)