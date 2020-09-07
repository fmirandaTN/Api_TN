from django.db import models

class Picture(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # file = models.FileField()
    storage_url = models.CharField(max_length=250)
    path_in_storage = models.CharField(max_length=250)
    owner = models.ForeignKey(
        'api.User', related_name="owner_picture", on_delete=models.CASCADE, null=True)
