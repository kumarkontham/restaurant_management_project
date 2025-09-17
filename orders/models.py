from django.db import models

# Create your models here.
class OrderStatus(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name
class Order(models.Model):
    status = models.ForeignKey('OrderStatus',on_delete = models.SET_Null,null=True,blank=True,related_name='orders')
    def __str__(self):
        return f"{self.pk} {self.status}"
