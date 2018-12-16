from django.db import models
#from djangotoolbox.fields import EmbeddedModelField
from pymongo import MongoClient
from django import template
#from django.contrib.postgres.fields import ArrayField


client = MongoClient()
db = client.test # BD
restaurants = db.restaurants # Coleccion

class Dish(models.Model):
    name = models.CharField(max_length=200)
    dish_type = models.CharField(max_length=100)
    allergens = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.name
    