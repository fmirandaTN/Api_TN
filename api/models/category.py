from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False)
    main_category = models.BooleanField(default=False)
    category = models.ForeignKey('self', related_name="father_category", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name