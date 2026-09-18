from django.shortcuts import render,redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm,CandidateProfileForm,RecruiterProfileForm
from accounts.models import CandidateProfile,RecruiterProfile
from django.contrib.auth.forms import AuthenticationForm
from applications.models import Application
from django.views.decorators.cache import never_cache
# Create your views here.
@never_cache
def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
         user=form.save()
         role=form.cleaned_data["role"]
         if role=="candidate":
          CandidateProfile.objects.create(user=user)
          login(request,user)
          return redirect("candidate_dashboard")
         elif role=="recruiter":
          RecruiterProfile.objects.create(user=user) 
          login(request,user)
          return redirect("recruiter_dashboard")
    else:
        form=UserRegistrationForm()
    return render(request, "accounts/register.html",{"form":form})

@never_cache
def candidate_profile(request):
 if request.user.is_authenticated:
    profile,created = CandidateProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST,request.FILES,
            instance=profile)
        if form.is_valid():
            form.save()
            return redirect("candidate")
    else:
        form = CandidateProfileForm(instance=profile)
    return render( request,"accounts/candidate_profile.html",
        {"form": form})
 else:
     return redirect("login")
 
@never_cache
def candidate_dashboard(request):
 if request.user.is_authenticated:
    try:
        candidate=CandidateProfile.objects.get(user=request.user)
        applications=Application.objects.filter(candidate=candidate)
        total_count=applications.count()
        pending_count=applications.filter(status="Pending").count()
        accepted_count=applications.filter(status="Accepted").count()
        rejected_count=applications.filter(status="Rejected").count()
        orderby=applications.order_by('-applied_at')[:5]
        context={
            'total_count':total_count,
            'pending_count':pending_count,
            'accepted_count':accepted_count,
            'rejected_count':rejected_count,
            'orderby':orderby
        }
        return render(request,"accounts/candidate_dashboard.html",context)
    except CandidateProfile.DoesNotExist: 
            return redirect("login")
 else:
    return redirect("login")

@never_cache
def recruiter_profile(request):
   if request.user.is_authenticated:
        try:
            profile= RecruiterProfile.objects.get(user=request.user)
        except RecruiterProfile.DoesNotExist:
                return redirect("login")
        if request.method=='POST':
            form= RecruiterProfileForm(request.POST,instance=profile)
            form.instance.user = request.user
            if form.is_valid():
                form.save()
                return redirect("recruiter")
        else:
            form=RecruiterProfileForm(instance=profile)
        return render(request,"accounts/recruiter_profile.html",{"form": form})
   else:
       return redirect("login")

@never_cache
def login_view(request):
   if request.method=='POST':
      form=AuthenticationForm(request, data=request.POST)
      if form.is_valid():
         user=form.get_user()
         login(request,user)
         try:
             profile= CandidateProfile.objects.get(user=request.user)
             return redirect("candidate_dashboard")
         except CandidateProfile.DoesNotExist:
                try:
                    profile= RecruiterProfile.objects.get(user=request.user)
                    return redirect("recruiter_dashboard")
                except RecruiterProfile.DoesNotExist:
                    return redirect("register")
   else:
     form=AuthenticationForm()
   return render(request, "accounts/login.html",{"form":form})

def home(request):
    return render(request, "home.html")