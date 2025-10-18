from django.db import models

class Manual(models.Model):
    file = models.FileField(upload_to="manuals/%Y/%m/%d/")
    filename = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_type = models.CharField(
        max_length=50,
        choices=[("technician","Technician"),("user","Common User")],
        default="user"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.filename