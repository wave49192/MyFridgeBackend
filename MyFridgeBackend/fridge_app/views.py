from django.shortcuts import render

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view


from MyFridgeBackend.fridge_app.serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
@api_view(['GET'])
def getFoodData(request):
    foodList = {'name': 'Fried chicken', 'cookingTime': 30}
    return Response(foodList)