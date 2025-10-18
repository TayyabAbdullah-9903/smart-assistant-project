from django.db import models
from manuals.models import Manual

class UMLDiagram(models.Model):
    manual = models.ForeignKey(Manual, on_delete=models.SET_NULL, null=True, blank=True)
    diagram_type = models.CharField(max_length=50)  # activity/sequence/component/usecase
    puml_code = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
