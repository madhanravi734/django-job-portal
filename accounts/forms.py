from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CandidateProfile,RecruiterProfile

PROFILE_CHOICES=[('candidate','Candidate'),('recruiter','Recruiter')]
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    role=forms.ChoiceField(choices=PROFILE_CHOICES,label="Choose an option")
class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ('phone','experience','skills'
                  ,'resume','education')
class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ('company_name','company_description'
                  ,'company_website')

