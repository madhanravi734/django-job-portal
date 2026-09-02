from django.shortcuts import render,redirect
from .models import CandidateProfile,Job,Application
from accounts.models import RecruiterProfile
from .forms import ApplicationForm
from django.views.decorators.cache import never_cache
# Create your views here.

@never_cache
def apply_job(request,job_id):
    if request.user.is_authenticated:
        try:
            job=Job.objects.get(id=job_id)
            candidate=CandidateProfile.objects.get(user=request.user)
            already_applied=Application.objects.filter(candidate=candidate,
                                                    job=job).exists()
            if already_applied:
                return redirect("job_list")
        except CandidateProfile.DoesNotExist:
            return redirect("login")
        except Job.DoesNotExist:
            return redirect("job_list")
             
        Application.objects.create(candidate=candidate,job=job)
        return redirect("job_detail",id=job.id)
    else:
        return redirect("login")

@never_cache
def view_applicants(request,job_id):
     if request.user.is_authenticated:
        try:
            recruiter=RecruiterProfile.objects.get(user=request.user)
            job=Job.objects.get(id=job_id)
            if job.recruiter==recruiter:
                applicants=Application.objects.filter(job=job)
                context={
                    'applicants':applicants
                }
                return render(request,"applications/applicants.html",context)
            else:
                return redirect("login")
        except RecruiterProfile.DoesNotExist:
            return redirect("login")
        except Job.DoesNotExist:
            return redirect("job_list")
     else:
       return redirect("login")
     
@never_cache
def update_status(request, application_id):
    if request.user.is_authenticated:
      try:
        recruiter=RecruiterProfile.objects.get(user=request.user)
        application=Application.objects.get(id=application_id)
        if application.job.recruiter==recruiter:
            if request.method == "POST":
                form=ApplicationForm(request.POST,instance=application)
                if form.is_valid():
                    form.save()
                    return redirect("view_applicants", job_id=application.job.id)
            else:
                return redirect("view_applicants",job_id=application.job.id)
        else:
            return redirect("login")
      except RecruiterProfile.DoesNotExist:
        return redirect("login")
      except Application.DoesNotExist:
        return redirect("job_list")
    else:
        return redirect("login")

@never_cache
def my_applications(request):
    if request.user.is_authenticated:
        try:
                candidate=CandidateProfile.objects.get(user=request.user)
                apply_cand=Application.objects.filter(candidate=candidate)
                context={
                    'apply_cand':apply_cand
                }
                return render(request,'applications/my_applications.html',context)
        except CandidateProfile.DoesNotExist:
            return redirect("login")
    else:
     return redirect("login")