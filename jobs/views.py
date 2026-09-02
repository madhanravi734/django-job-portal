from django.shortcuts import render,redirect
from accounts.models import RecruiterProfile
from jobs.forms import JobForm
from jobs.models import Job
from applications.models import Application
from django.views.decorators.cache import never_cache
# Create your views here.

@never_cache
def create_job(request):
    if request.user.is_authenticated:
        try:
            recruiter=RecruiterProfile.objects.get(user=request.user)
        except RecruiterProfile.DoesNotExist:
            return redirect("login")
        if request.method=='POST':
               form= JobForm(request.POST)
               if form.is_valid():
                   job= form.save(commit=False)
                   job.recruiter=recruiter
                   job.save()
                   return redirect("my_jobs")
        else:
            form=JobForm()
    else:
        form=JobForm()
        return redirect("login")
    return render(request, "jobs/job_create.html", {"form": form})

@never_cache
def job_list(request):
    jobs=Job.objects.all()
    context={
        'jobs':jobs
    }
    return render(request,'jobs/job_list.html',context)

@never_cache
def job_detail(request,id):
  try:
    job=Job.objects.get(id=id)
    return render(request, "jobs/job_detail.html", {"job": job})
  except Job.DoesNotExist:
       return redirect("job_list")

@never_cache
def my_jobs(request):
 if request.user.is_authenticated:
        try:
            recruiter=RecruiterProfile.objects.get(user=request.user)
            jobs=Job.objects.filter(recruiter=recruiter)
            context={
                'jobs':jobs
            }
            return render(request,'jobs/my_jobs.html',context)
        except RecruiterProfile.DoesNotExist:
                    return redirect("login")
 else:
      return redirect("login")

@never_cache
def edit_job(request,id):
    if request.user.is_authenticated:
        try:
            jobs=Job.objects.get(id=id)
            recruiter=RecruiterProfile.objects.get(user=request.user)
            if jobs.recruiter==recruiter:
             if request.method == "POST":
                        form=JobForm(request.POST,instance=jobs)
                        if form.is_valid():
                            form.save()

                            return redirect("my_jobs")
             else:
                form=JobForm(instance=jobs)
                context={
                    'form':form
                }
                return render(request,"jobs/edit_job.html",context)
            else:
                return redirect("login")
        except RecruiterProfile.DoesNotExist: 
            return redirect("login")
        except Job.DoesNotExist: 
            return redirect("my_jobs")
    else:
        return redirect("login")

@never_cache
def delete_job(request,id):
    if request.user.is_authenticated:
        try:
            jobs=Job.objects.get(id=id)
            recruiter=RecruiterProfile.objects.get(user=request.user)
            if jobs.recruiter==recruiter:
                if request.method == "POST":
                    jobs.delete()
                    return redirect("my_jobs")
                else:
                    return redirect("login")
            else:
                return redirect("my_jobs")
        except RecruiterProfile.DoesNotExist: 
            return redirect("login")
        except Job.DoesNotExist: 
            return redirect("my_jobs")
    else:
            return redirect("login")
@never_cache
def recruiter_dashboard(request):
    if request.user.is_authenticated:
        try:
            recruiter=RecruiterProfile.objects.get(user=request.user)
            jobs=Job.objects.filter(recruiter=recruiter)
            total_count=jobs.count()
            total_applicants=Application.objects.filter(job__in=jobs).count()
            pending_count=Application.objects.filter(status="Pending",job__in=jobs).count()
            accepted_count=Application.objects.filter(status="Accepted",job__in=jobs).count()
            rejected_count=Application.objects.filter(status="Rejected",job__in=jobs).count()
            orderby=Application.objects.filter(job__in=jobs).order_by('-applied_at',)[:5]
            context={
                    'total_count':total_count,
                    'total_applicants':total_applicants,
                    'pending_count':pending_count,
                    'accepted_count':accepted_count,
                    'rejected_count':rejected_count,
                    'orderby':orderby
                }
            return render(request,"accounts/recruiter_dashboard.html",context)
        except RecruiterProfile.DoesNotExist: 
                    return redirect("login")
    else:
         return redirect("login")