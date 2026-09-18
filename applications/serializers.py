from rest_framework import serializers
from .models import Application
class ApplicationSerializer(serializers.ModelSerializer):
    candidate = serializers.PrimaryKeyRelatedField(read_only=True)
    job = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=Application
        fields=['candidate','job','applied_at','status']