from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
class MenuItems(models.Model):
    menu_name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    def __str__(self):
        return self.menu_name
class Feedback(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}-{self.cooment}"
class MenuCategory(models.Model):
    name = models.CharField(max_length=100,unique=True)
    
