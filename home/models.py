from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class MenuItems(models.Model):
    mname = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    def __str__(self):
        return self.mname