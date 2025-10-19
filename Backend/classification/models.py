from django.db import models
from manuals.models import Manual
from chatbot.models import ChatQuery

class PIClassification(models.Model):
    manual = models.ForeignKey(Manual, on_delete=models.CASCADE, related_name="classifications", null=True, blank=True)
    query = models.ForeignKey(ChatQuery, on_delete=models.CASCADE, related_name="pi_classifications", null=True, blank=True)

    # Four PI-Class categories
    intrinsic_product = models.CharField(max_length=255, blank=True, null=True)
    extrinsic_product = models.CharField(max_length=255, blank=True, null=True)
    intrinsic_information = models.CharField(max_length=255, blank=True, null=True)
    extrinsic_information = models.CharField(max_length=255, blank=True, null=True)

    # Auto-generated summary
    summary = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PI-Class for {self.query or self.manual}"
