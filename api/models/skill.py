from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        'api.Category', on_delete=models.CASCADE, related_name="skill", blank=False)

    def category_name(self):
        return self.category.name