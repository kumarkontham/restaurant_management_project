from urllib.parse import quote_plus
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
from django.core.mail import send_mail
#settings.py
RESTAURANT_ADDRESS = "1/34 road no:12 hyderabad area"
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
def faq_view(request):
    return render(request,"home/faq.html")
def home_view(request):
    if request.method =="GET":
        query = request.GET.get('q')
        if query:
            search_items=Menu_items.objects.filter(name__contains=query)
    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name =form.cleaned_data["name"]
            email=form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            subject= f"new contact form from {name}"
            send_mail(
                subject,
                settings.DEFAULT.FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
            )
            form.save()
            return render(request,"home/contact_success.html")
        else:
            form = ContactForm()
    location = Location.objects.first()
    restaurant=Restaurant.objects.first()

    restaurant_name=restaurant.restaurant_name if restaurant else settings.RESTAURANT_NAME 
    address = restaurant.address if restaurant else settings.RESTAURANT_ADDRESS
    map_src=None
    maps_link = f"https://www.google.com/maps/search/?api=1&query={quote_plus(address)}"if address else None
    context = {"restaurant_name":restaurant_name,"restaurant_address":address,"maps_link":maps_link,"form":form,"location":location}
    return render(request,"home/home.html",context)
def menu_view(request):
    menu_items = Menuitem.objects.all()
    context = {"menu_items":menu_items}
    return render(request,"home/menu.html",context)
def restaurant_info_view(request):
    context = {"history":"our restaurant is founded in 1995 with a vision of serving authenic local flavors",
    "mission":"To deliver exceptional culinary experiences in a warm, wellcomming environment."}
    return render(request,"home/about.html", context)
def add_to_cart(request,product_id):
    cart = get_or_create_cart(request)
    menu_item = get_object_or_404(Menuitem,id=product_id)
    item,created = CartItem.objects.get_or_create(cart = cart ,menu_item=menu_item)
    if not created:
        item.quantity+=1
        item.save()
    return redirect(menu_view)
    
# class Feedback(models.Model):
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.id}-{self.comment}"
#models.py
class Restaurant(models.Model):
    name=models.CharField(max_length=30,blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    Mobile_number = models.CharField(max_length=15)
    opening_hours = models.JSONField(default=dict)
    logo = models.ImageField(upload_to="menu_items/",blank=True,null=True)
    def __str__(self):
        return f"{self.name}" 
class Menuitem(models.Model):
    item_name = models.CharField(max_length=40)
    description = models.TextField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    image = models.ImageField(upload_to = 'menu_items/',blank=True,null=True)
    def __str__(self):
        return self.item_name
class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(required=True,unique=True)
    message = models.TextField(required=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}-{self.email}"
class Location(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=6)
    def __str__(self):
        return f"{self.address}"
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
class CartItem(models.Model):
    menu_item = models.ForeignKey(Menuitem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} {self.menu_item.name}"
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
class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=["name","email","message"]
#contextprocessors.py
def cart_items_count(request):
    cart = get_or_create_cart(request)
    return {"cart_item_count":cart.total_items}
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
]
def display_success_message():
    return "basic css styles added  successfully for the home page"  
if __name__ == "__main__":
    print(display_success_message())