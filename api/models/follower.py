from django.db import models

class Follower(models.Model):
    owner = models.ForeignKey(
        'api.User', related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(
        'api.User', related_name="following", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("owner", "following"),)
