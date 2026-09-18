from django.urls import path
from . import views

urlpatterns = [
   path('apply/<int:job_id>/',views.apply_job,name="apply_job"),
   path('applicants/<int:job_id>/',views.view_applicants,name="view_applicants"),
   path('update-status/<application_id>/',views.update_status,name="update_status"),
   path('my-applications/',views.my_applications,name="my_applications"),
   path('apply_job_api/<int:job_id>/',views.apply_job_api,name="apply_job_api"),
   path('application_list_api/',views.application_list_api,name="application_list_api"),
   path('application_detail_api/<int:application_id>/',views.application_detail_api,name="application_detail_api"),
   ]
