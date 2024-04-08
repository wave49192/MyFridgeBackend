from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from Inventory.models import Ingredient, Inventory, InventoryItem
from Inventory.serializers import IngredientSerializer, InventoryItemSerializer, InventorySerializer

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
    
class InventoryItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    
    def list(self, request):
        queryset = InventoryItem.objects.all()
        serializer = InventoryItemSerializer(queryset, many=True)
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
    
    @action(detail=True, methods=['post'], url_path='ingredients')
    def add_ingredients(self, request, pk):
        inventory = self.get_object()
        serialized_ingredient_ids = InventoryItemSerializer(many=True, data=request.data.get('ingredients'))
        serialized_ingredient_ids.is_valid(raise_exception=True)

        try:
            for item in request.data.get('ingredients'):
                ingredient, quantity, unit = item.values()
                inventory_item = InventoryItem.objects.create(ingredient_id=ingredient, quantity=quantity, unit=unit)
                inventory.items.add(inventory_item)
                inventory.save()
            serializer = self.serializer_class(inventory)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    @action(detail=False, methods=['get'], url_path='user')
    def user(self, request):
        if not request.query_params.get('user_id').isnumeric():
            raise NotFound("Inventory not found.")
        
        inventory = Inventory.objects.filter(owned_by=request.query_params.get('user_id')).first()
        
        if not inventory:
            raise NotFound("Inventory not found.")
        
        serializer = self.serializer_class(inventory)

        return Response(serializer.data)