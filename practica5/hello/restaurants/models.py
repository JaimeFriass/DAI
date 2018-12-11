from django.db import models
#from djangotoolbox.fields import EmbeddedModelField
from pymongo import MongoClient
from django import template

client = MongoClient()
db = client.test # BD
restaurants = db.restaurants # Coleccion