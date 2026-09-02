from django.urls import path
from . import views
urlpatterns = [
   path('create_jobs/',views.create_job,name="job_create"),
   path('job_list/',views.job_list,name="job_list"),
   path('job_detail/<int:id>/',views.job_detail,name="job_detail"),
   path('my_jobs/',views.my_jobs,name="my_jobs"),
   path('edit_job/<int:id>/',views.edit_job,name="edit_job"),
   path('delete_job/<int:id>/',views.delete_job,name="delete_job"),
   path('recruiter-dashboard/',views.recruiter_dashboard,name="recruiter_dashboard"),
   ]