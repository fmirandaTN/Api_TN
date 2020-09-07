from django.db import models
from api.models import Project
from django.core.validators import MaxValueValidator, MinValueValidator

class Rating(models.Model):
    type_choices = [
        ('collaborator', 'collaborator'),
        ('client', 'client')]
        
    # Client or collaborator
    rating_type = models.CharField(max_length=50, choices=type_choices)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=1000)

    rating_average = models.IntegerField(default = 0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    rating_communication = models.IntegerField(default = 0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    rating_quality =  models.IntegerField(default = 0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    rating_punctuality =  models.IntegerField(default = 0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    rating_agreed_terms = models.IntegerField(default = 0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    rating_clarity =  models.IntegerField(default = 0,validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = (("rating_type", "project"),)