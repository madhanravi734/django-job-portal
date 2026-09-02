from django.urls import path
from . import views

urlpatterns = [
   path('apply/<int:job_id>/',views.apply_job,name="apply_job"),
   path('applicants/<int:job_id>/',views.view_applicants,name="view_applicants"),
   path('update-status/<application_id>/',views.update_status,name="update_status"),
   path('my-applications/',views.my_applications,name="my_applications"),]
