from django.db import models

from Authentication.models import User

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=50)
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
    
class InventoryItem(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=20, default='')

class Inventory(models.Model):
    items = models.ManyToManyField(InventoryItem, default=[], blank=True)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.owned_by)
