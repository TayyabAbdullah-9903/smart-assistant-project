from django.db import models
from manuals.models import Manual

class ChatQuery(models.Model):
    manual = models.ForeignKey(Manual, on_delete=models.SET_NULL, null=True, blank=True)
    query_text = models.TextField()
    user_type = models.CharField(
        max_length=50,
        choices=[("technician", "Technician"), ("user", "Common User")],
        default="user"
    )
    response_text = models.TextField(null=True, blank=True)
    uml_code = models.TextField(null=True, blank=True)
    diagram_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.CharField(max_length=10, null=True, blank=True, default="Good")

    # ✅ new fields for Colab / export integration
    puml_file = models.FileField(upload_to="uml_files/", null=True, blank=True)
    py_file = models.FileField(upload_to="uml_files/", null=True, blank=True)
    txt_file = models.FileField(upload_to="uml_files/", null=True, blank=True)

    def __str__(self):
        return f"Query {self.id} ({self.user_type})"
