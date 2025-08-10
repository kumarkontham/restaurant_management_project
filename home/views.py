from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Restaurant,MenuItems
def home_page(request):
    """display restaurantname on the home page
    fetch from the database if available otherwise get the name from settings file
    after accessing the name this view rendering to the home.html template to show the data in staic pages."""
    restaurant = Restaurant.objects.first()
    restaurant_name = restaurant.name if restaurant else getattr(settings,"RESTAURANT_NAME","culture food")
    return render(request,'home/home.html',{"restaurant_name":restaurant_name})
def get_restaurant_name(request):
    """display the restaurant name in Json format"""
    restaurant = Restaurant.objects.first()
    if not restaurant:
        return render(request,'custom_404.html')
    else:
        name = restaurant.name
        return render(request,'home/home.html',{"name":name})

    


    
