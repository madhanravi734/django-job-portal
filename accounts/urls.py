from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
   path('register/',views.register,name="register"),
   path('candidate-profile/',views.candidate_profile,name="candidate"),
   path('recruiter-profile/',views.recruiter_profile,name="recruiter"),
   path('login/',views.login_view,name="login"),
   path('logout/',LogoutView.as_view(next_page="login"),name="logout"),
   path('candidate-dashboard/',views.candidate_dashboard,name="candidate_dashboard"),
]