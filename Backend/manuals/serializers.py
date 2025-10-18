from rest_framework import serializers
from .models import Manual

class ManualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manual
        fields = "__all__"
        read_only_fields = ("uploaded_at","processed")
