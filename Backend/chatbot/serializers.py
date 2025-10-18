from rest_framework import serializers
from .models import ChatQuery

class ChatQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatQuery
        fields = "__all__"
        read_only_fields = ("response_text","uml_code","diagram_url","created_at")
