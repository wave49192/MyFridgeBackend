from rest_framework import permissions, viewsets
from rest_framework.response import Response

from Inventory.models import Ingredient, Inventory
from Inventory.serializers import IngredientSerializer, InventorySerializer

# Create your views here.
class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
    def list(self, request):
        queryset = Ingredient.objects.all()
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data)
    
class InventoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    
    def list(self, request):
        queryset = Inventory.objects.all()
        serializer = InventorySerializer(queryset, many=True)
        return Response(serializer.data)