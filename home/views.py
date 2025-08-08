from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from .models import Restaurant
from rest_framework.response import Response
@api_view(['GET'])
def home_page(request):
    return render(request,'home/home.html')
class RestaurantNameAPI(APIView):
    def get(self,request):
        restaurant = Restaurant.objects.first()
        name = restaurant.name if restaurant else settings.RESTAURANT_NAME
        return Response({"name":name})
def homepage(request):
    restaurant = Restaurant.objects.first()
    restaurant = restaurant.name if restaurant else settings.RESTAURANT_NAME
    return render(request,'home/home.html',{'restaurant_name':name})
    
