from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Restaurant
from .forms import ContactForm
def home_page(request):
    """display restaurantname on the home page
        fetch from the database if available otherwise get the name from settings file """
    restaurant = Restaurant.objects.first()
    restaurant_name = restaurant.name if restaurant else getattr(settings,"RESTAURANT_NAME","culture food")
    contact_number = restaurant.phone if restaurant else getattr(settings,"RESTAURANT_CONTACT","+91-6785432162")
    return render(request,'home/home.html',{"restaurant_name":restaurant_name,"contact":contact_number})
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
def Contact_us(request):
    submitted = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            submitted =True
    else:
        form = ContactForm()
    context = {
        "form":form,
        'submitted':submitted,
        'contact_email':'kk@gmail.com',
        'contact_phone':'87575735322',
        'contact_address':'karimnagar',
    }
    return render(request,'home/Contact_us.html',context)

def Menu_items(request):
    Menu_Items = [{"id":1,"item_name":"chickeen_curry","price":"200.00"},
    {"id":2,"item_name":"sambar_rice","price":"99.00"},
    {"id":3,"item_name":"Tiffins","price":"30.00"},
    {"id":4,"item_name":"Drinks","price":"55.00"},]
    context = {'Menu_Items':Menu_Items}
    return render(request,'home/menu.html',context)
def reservation_view

    

    
