from rest_framework import permissions, viewsets

from Inventory.models import Ingredient
from Inventory.serializers import IngredientSerializer

# Create your views here.
class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer