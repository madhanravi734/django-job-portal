from rest_framework import serializers
from .models import Job
class JobSerializer(serializers.ModelSerializer):
  recruiter = serializers.PrimaryKeyRelatedField(read_only=True)
  def validate_salary(self,value):
         if value<0:
           raise serializers.ValidationError("Salary cannot be negative")
         return value
  def validate_title(self,value):
     if not value.strip():
        raise serializers.ValidationError("Give valid title")
     return value
  class Meta:
    model=Job
    fields=['recruiter','title','description','location',
            'salary','skills','created_at']