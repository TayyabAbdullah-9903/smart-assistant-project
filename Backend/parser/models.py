from django.db import models
from manuals.models import Manual

class ManualText(models.Model):
    manual = models.ForeignKey(Manual, on_delete=models.CASCADE, related_name="texts")
    page_index = models.IntegerField(null=True, blank=True)
    text = models.TextField()
    extracted_at = models.DateTimeField(auto_now_add=True)
