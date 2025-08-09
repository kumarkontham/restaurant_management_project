from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Restaurant,MenuItems
def home_page(request):
    """display restaurantname on the home page
        fetch from the database if available otherwise get the name from settings file """
    restaurant = Restaurant.objects.first()
    restaurant_name = restaurant.name if restaurant else getattr(settings,"RESTAURANT_NAME","culture food")
    return render(request,'home/home.html',{"restaurant_name":restaurant_name})
@api_view(["GET"])
def get_restaurant_details(request):
    """display the restaurant name in Json format"""
    restaurant = Restaurant.objects.first()
    name = restaurant.name if restaurant else getattr(settings,"RESTAURANT_NAME","culture food")
    return Response({"name":name})
def get_restaurant_name():
    return getattr(settings,"RESTAURANT_NAME","culture food")
def about_us(request):
    name=get_restaurant_name()
    description=f"welcome to {name} restaurant!"
    "Here we are providing service for delicious and freshly prepared meals"
    "with ingredients from local farms.Our goal is to provide healthy and tasty food "
    return render(request,"home/about.html",{"restaurant_name":name})
def hardcoded_items(request):
    """create the hardcoded list  """
    menu_items = [{"id" : 1,"mname" : "Starters" ,"url" : '#'},
    {"id" : 2,"mname" : "Mains","url" : "#"},
    {"id" : 3,"mname" : "Desserts","url" : "#"},
    {"id" : 4,"mname" : "Drinks","url" : "#"}]
    return render(request, 'home/menu.html', {"menu_items" : menu_items})
    


    
