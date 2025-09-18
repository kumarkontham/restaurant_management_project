from rest_framework import serializers 
from .models import MenuCategory

class MenuCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ["name"]
        