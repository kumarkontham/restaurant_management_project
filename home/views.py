from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from .models import Restaurant
from rest_framework.response import Response
from django.views.decorators.http import require_GET
@api_view(["GET"])
def get(self,request):
    restaurant = Restaurant.objects.first()
    name = restaurant.name if restaurant else settings.RESTAURANT_NAME
    return Response({"name":name})
def home_page(request):
    restaurant = Restaurant.objects.first()
    restaurant = restaurant.name if restaurant else settings.RESTAURANT_NAME
    return render(request,'home/home.html',{'restaurant_name':name})
    
