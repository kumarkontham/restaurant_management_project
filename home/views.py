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
@api_view(["GET"])
def get_restaurant_details(request):
    """display the restaurant name in Json format"""
    
    restaurant = Restaurant.objects.first()
    if not restaurant:
        return Response({"error":"No Restaurant found"},status=404)
    name = restaurant.name
    return Response({"name":name})
def get_restaurant_name():
    return getattr(settings,"RESTAURANT_NAME","culture food")
def about_us(request):
    name=get_restaurant_name()
    description=f"welcome to {name} restaurant! Here we are providing service for delicious and freshly prepared meals with ingredients from local farms. Our goal is to provide healthy and tasty food "
    return render(request,"home/about.html",{"restaurant_name":name,"description":description})
def hardcoded_items(request):
    """create the hardcoded list inside the list menu items are added in dictionary format key,value pairs whenever user wants to retrieve the data using the template file   """
    menu_items = [{"id" : 1,"menu_name" : "Starters" ,"url" : '#'},
    {"id" : 2,"menu_name" : "Mains","url" : "#"},
    {"id" : 3,"menu_name" : "Desserts","url" : "#"},
    {"id" : 4,"menu_name" : "Drinks","url" : "#"}]
    return render(request, 'home/menu.html', {"menu_items" : menu_items})
    


    
