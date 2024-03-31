from rest_framework import permissions, viewsets

from Inventory.models import Ingredient, Inventory
from Inventory.serializers import IngredientSerializer, InventorySerializer

# Create your views here.
class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
class InventoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer