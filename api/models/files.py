from django.db import models

class ProjectFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.CharField(max_length=250)
    original_name = models.CharField(max_length=250)
    owner = models.ForeignKey( 
        'api.User', related_name="owner_file", on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(
        'api.Project', on_delete=models.CASCADE, null=True)
