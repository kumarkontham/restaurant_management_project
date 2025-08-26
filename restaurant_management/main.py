from django.db import models
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.urls import path
from rest_framework.views import APIView
from rest_framework import serializers
from django.urls import reverse
# COPYRIGHT="\u00A9 | 2025 All Rights Reserved"
# OPENING_HOURS = "Mon-Fri:9:00am-9:00pm,Sat-Sun:10:00am-10:00pm"
# def home_page_rendering(title:str,body:str):
#     html=f"""<!DOCTYPE html>
#     <html lang="en">
#     <head>
#     <title>{title}</title>
#     </head>
#     <body>
#     <header>
#     <h2>Welcome to my Restaurant</h2>
#     </header>
#     <main>
#     {body}
#     </main>
#     <footer>
#     <small>Openings hours:{OPENING_HOURS}</small>
#     <span>{COPYRIGHT}</span>
#     </footer>
#     </body>
#     </html>
#     """
#     return HttpResponse(html)
#views.py
def home_view(request):
    restaurant=Restaurant.objects.first()
    restaurant_name=restaurant.restaurant_name if restaurant else settings.RESTAURANT_NAME 
    context={"restaurant_name":restaurant_name}
    return render(request,"home/home.html",context)
def menu_view(request):
    menu_items = Menuitem.objects.all()
    return render(request,"home/menu.html")
# class Feedback(models.Model):
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.id}-{self.comment}"
#models.py
class Restaurant(models.Model):
    name=models.CharField(max_length=30,blank=True,null=True)
    def __str__(self):
        return f"{self.name}" 
class Menuitem(models.Model):
    item_name = models.CharField(max_length=40)
    description = models.TextField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    def __str__(self):
        return self.item_name
"""Run the commands for update data in the database 
python manage.py makemigrations
python manage.py migrate"""  
# class Orders(models.Model):
#     STATUS_PENDING="pending"
#     STATUS_COMPLETED="completed"
#     STATUS_IN_PROGRESS="in_progress"
#     STATUS_CANCELED = "canceled"
#     STATUS_CHOICES =[
#     (STATUS_PENDING,"pending"),
#     (STATUS_IN_PROGRESS,"in_progress"),
#     (STATUS_COMPLETED,"completed"),
#     (STATUS_CANCELED,"canceled"),
#     ]
#     customer = models.ForeignKey(User,on_delete=CASCADE,related_name='orders')
#     total_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
#     status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending")
#     def __str__(self):
#         return f"order #{self.id} by {self.customer}"
# class Menu_items(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
#     def __str__(self):
#         return self.name
# class User_profile(models.Model):
#     user = models.OneToOneField(User,on_delete=CASCADE)
#     email = models.EmailField(unique=True)
#     Mobile_number = models.CharField(max_length=15,blank=True)
#     def __str__(self):
#         return self.user.username
#serializers.py
# class Menu_items_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Menu_items
#         fields="__all__"
#forms.py
# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ["comment"]
#         widgets = {
#             "comment": forms.Textarea(attrs={"rows":4,"placeholder":"Enter your feedback."})
#         }
# #views.py
# def feedback_view(request):
#     if request.method == "POST":
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("feed_back_completed")
#     else:
#         form = FeedbackForm()
#     return render(request,'home/feedback.html',{"form":form})
# def feed_back_completed(request):
#     return HttpResponse("<h2>Thank you for your response.</h2>")
# class MenuAPIView(APIView):
#     def get(self,request):
#         menu = [{"name":"chicken biryani","description":"fresh chicken with made up of with self made ingredients","price":300},
#         {"name":"smabarrice","description":"home style food","price":99},
#         {"name":"tiffins","description":"all tiffins avalable","price":45},
#         ]
#         return Response(menu,status=status.HTTP_200_OK)
# class Menu_itemsAPI_view(APIView):
#     def get(self,request,format=None):
#         items = Menu_items.objects.all()
#         serializer = Menu_items_serializer(items,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
# def menu_view(request):
#     api_url = request.build_abolute_url(reverse('menu_api'))
#     try:
#         resp = requests.get(api_url,timeout=5)
#         resp.raise_for_status()
#         menu_items = resp.json()
#     except requests.RequestException:
#         menu_items=[]
#     return render(request,"home/home.html",{"menu_items":menu_items})

#urls.py
urlpatterns =[
    path("",views.home_view,name = "home_page"),
    path("menu/",views.menu_view,name="menu_items"),
    # path("feedback/",views.feedback_view,name="feedback_form"),
    # path("menu/",views.MenuAPIView.as_view(),name="menu_items"),
    # path("menu_items/",Menu_itemsAPI_view.as_view(),name="menu_api"),
]
def display_success_message():
    return "basic css styles added  successfully for the home page"  
if __name__ == "__main__":
    print(display_success_message())