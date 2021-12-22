from django.db import models
from django.db.models.fields import FloatField

class productmodel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField( max_length=200 )
    description = models.CharField( max_length=400 )
    price = FloatField()
    class Meta:
       db_table = "product" 
