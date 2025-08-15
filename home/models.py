from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    logo = models.ImageField(upload_to='logos/',blank=True,null=True)

    def __str__(self):
        return self.name
