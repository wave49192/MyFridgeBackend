from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    
class User(models.Model):
    name = models.CharField(max_length=100)
    
class Inventory(models.Model):
    ingredients = models.ManyToManyField(Ingredient)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    