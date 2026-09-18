from django.shortcuts import render,redirect
from .models import CandidateProfile,Job,Application
from accounts.models import RecruiterProfile
from .forms import ApplicationForm
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApplicationSerializer
from .permissions import IsCandidate,IsApplicationJobOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
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

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsCandidate])
def apply_job_api(request, job_id):
      try:
        job=Job.objects.get(id=job_id)
      except Job.DoesNotExist:
        return Response("Job not found",status=status.HTTP_404_NOT_FOUND)
      candidate=CandidateProfile.objects.get(user=request.user)
      already_applied=Application.objects.filter(candidate=candidate,job=job).exists()
      if already_applied:
            return Response({"detail": "You have already applied for this job."},status=status.HTTP_400_BAD_REQUEST)
      application=Application.objects.create(candidate=candidate,job=job)
      serializer=ApplicationSerializer(application)
      return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_list_api(request):
    if hasattr(request.user,'candidateprofile'):
        application=Application.objects.filter(candidate__user = request.user)
    elif hasattr(request.user,'recruiterprofile'):
            application=Application.objects.filter(job__recruiter__user = request.user)
    else:
         return Response(status=status.HTTP_403_FORBIDDEN)
    serializer=ApplicationSerializer(application,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def application_detail_api(request,application_id):
    try:
     application=Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return Response("Application not found",status=status.HTTP_404_NOT_FOUND)
    if request.method=="GET":
     if request.user ==application.candidate.user or request.user ==application.job.recruiter.user:
        serializer=ApplicationSerializer(application)
        return Response(serializer.data,status=status.HTTP_200_OK)
     else:
          return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.method=="PATCH":
            permission = IsApplicationJobOwner()
            if not permission.has_object_permission(request, None, application):
                return Response(
                    {"detail": "You do not have permission to modify this application."},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer=ApplicationSerializer(application,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)