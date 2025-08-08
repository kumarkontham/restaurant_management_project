from django.shortcuts import render
from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import api_view
from .models import Restaurant
def home_page(request):
    """display restaurantname on the home page """
    restaurant = Restaurant.objects.first()
    restaurant_name = restaurant.name if restaurant else settings.RESTAURANT_NAME
    return render(request,'home/home.html',{"restaurant_name":restaurant_name})
@api_view(["GET"])
def get_restaurant_details(request):
    restaurant = Restaurant.objects.first()
    name = restaurant.name if restaurant else settings.RESTAURANT_NAME
    return Response({"name":name})

    
