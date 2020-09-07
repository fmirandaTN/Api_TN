from api.models import Category
from rest_framework import viewsets, permissions
from api.serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated
from ..authentication import ExpiringTokenAuthentication


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    http_method_names = ['get']

    def get_queryset(self):
        self.queryset = Category.objects.all()
        category = self.queryset
        if self.request.query_params.keys():
            if 'main' in self.request.query_params.keys():
                if self.request.query_params['main'] == 'true':
                    category = Category.objects.filter(main_category=True)
                else:
                    category = Category.objects.filter(main_category=False)

            if 'sub-category' in self.request.query_params.keys():
                category = Category.objects.filter(category=self.request.query_params['sub-category'])
                
        return category