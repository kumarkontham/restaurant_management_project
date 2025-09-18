from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Restaurant,MenuItems
from rest_framework import status
form .serializres import MenuCategorySerializer
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
    name = restaurant.name if restaurant else getattr(settings,"RESTAURANT_NAME","culture food")
    return JsonResponse("restaurant_name":name)
def feedback_view(request):
    if request.method =="POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_thanks_view')
        else:
            form = FeedbackForm()
        return render(request,"home/feedback.html",{"form":form})
def feedback_thanks_view(request):
    return HttpResponse("<h2>Thank you for submitting your response</h2>")
class MenuAPIView(APIView):
    def get(self,request):
        menu = [{"name":"chicken biryani","description":"fresh chicken in used self made masala","price":300},{"name":"SambarRice","description":"home style preparation","price":199},{"name":"tiffin","description":"all types of  tiffins","price":45}]
        return Response(menu,status=status.HTTP_200_OK)



    


    
