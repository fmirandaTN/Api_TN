from rest_framework import serializers
from api.models import Project, Rating
    
class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('id','rating_average', 'rating_type', 'project',
                'rating_communication', 'rating_quality', 'rating_punctuality',
                'rating_agreed_terms', 'rating_clarity', 'comment')