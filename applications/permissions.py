from rest_framework.permissions import BasePermission

class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'candidateprofile')
        )

class IsApplicationJobOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.job.recruiter.user==request.user