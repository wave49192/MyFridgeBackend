"""
URL configuration for MyFridgeBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from Authentication.views import GoogleLoginApi, UserViewSet
from RecommendationSystem import views
from Inventory.views import IngredientViewSet, InventoryViewSet
from IngredientDetection.views import detectIngredients

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include(router.urls)), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('recipes/', views.getRecipe, name ='get_recipe'),
    path('ingredient/', views.getIngredients, name ='get_ingredient'),
    path('recipes/search/', views.searchRecipe, name='search_recipe'),
    path('detect/', detectIngredients, name='detect_ingredients'),
    path("auth/", GoogleLoginApi.as_view(), name="login-with-google"),
    path('recipes/details/', views.getRecipeDetails, name='get_details'),
]

urlpatterns += router.urls