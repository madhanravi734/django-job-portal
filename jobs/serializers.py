from rest_framework import serializers
from .models import Job
class JobSerializer(serializers.ModelSerializer):
  recruiter = serializers.PrimaryKeyRelatedField(read_only=True)
  def validate_salary(self,value):
         if value<0:
           raise serializers.ValidationError("Salary cannot be negative")
         return value
  class Meta:
    model=Job
    fields=['recruiter','title','description','location',
            'salary','skills','created_at']
  def validate(self,data):
     title=data['title']
     if not title.strip():
        raise serializers.ValidationError("Give valid title")
        
     else:
        return data