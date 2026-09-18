from rest_framework.permissions import BasePermission

class IsJobOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.recruiter.user == request.user

class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user,'recruiterprofile')

class CheckUser(BasePermission):
    def has_permission(self, request, view):
        if request.method=="GET":
            return hasattr(request.user,'recruiterprofile') or hasattr(request.user,'candidateprofile')
        if request.method=="POST":
            return hasattr(request.user,'recruiterprofile')