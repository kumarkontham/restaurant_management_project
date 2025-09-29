import string 
import logging
import secrets
from urllib.parse import quote_plus
import email_validator import validate_email,EmailNotValidError
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
from django.contrib.auth import authenticate,login 
from rest_framework.generics import CreateAPIView
#settings.py
RESTAURANT_ADDRESS = "1/34 road no:12 hyderabad area"
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
    specials = Special.objects.all()
    location = Location.objects.first()
    restaurant=Restaurant.objects.first()
    restaurant_name=restaurant.restaurant_name if restaurant else settings.RESTAURANT_NAME 
    address = restaurant.address if restaurant else settings.RESTAURANT_ADDRESS
    map_src=None
    maps_link = f"https://www.google.com/maps/search/?api=1&query={quote_plus(address)}"if address else None
    context = {"restaurant_name":restaurant_name,"restaurant_address":address,"maps_link":maps_link,"form":form,"location":location,"specials":specials}
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
def login_view(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                messages.success(request,"login successfully!")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password!")
    else:
        form = LoginForm()
    return render(request,"login.html",{"form":"form"})
class ItemsCategory(APIView):
    def get(self,request,format=None):
        category_name = request.query_params.get('category',None)
        if category_name:
            menu_items=MenuItem.objects.filter(category__name__iexact=category_name)
        else:
            menu_items=MenuItem.objects.all()
        serializer=MenuCategorySerializer(menu_items,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class ListAPIView(generics.ListAPIView):
    query_set = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer 
def create_coupon():
    code = generate_coupon_code(length=12)
    coupon=Coupon.objects.create(code=code)
    return coupon
class MenuItemAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self,request,format=None):
        q=request.GET.get("q",None)
        query_set = Menu_items.objects.all()
        if q:
            queryset =query_set.filter(name__icontains=q)
        queryset = queryset.order_by("name")
        serializer = MenuItemSerializer(serializer.data)
        return Response(serializer.data)
class MenuItemUpdateView(APIView):
    permission_classes=[IsAdminUser]
    def put(self,request,pk,format=None):
        menu_item = get_object_or_404(MenuItem,pk=pk)
        serializer=MenuItemSerializer(menu_item,data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response({"error":"error while creating the menu item"},status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,pk,format=None):
        menu_item=get_object_or_404(Menuitem,pk=pk)
        serializer=MenuItemSerializer(menu_item,data=request.data,partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response({"error":"error while updating menuitem "},status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors)
class OredersAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-created_at')
        serializer=OrdersViewSerializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
class UserProfileViewset(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self,request):
        serializer = UserPrifileSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
def create_order(request):
    order = Order.objects.create(
        order_id=generate_unique_order_id(prefix="ORD")
    ) 
class ContactFormSubmissionView(CreateAPIView):
    queryset = ContactFormSubmission.objects.all()
    serializer_class = ContactFormSubmissionser
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,{"message":"ContactFormSubmittedSuccessfully."},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class NotifyUser(APIView):
    def post(self,request):
        order_items = Order.objects.all()
        email = request.data.get('email')
        order_id = request.data.get('order_id')
        message = "Thank you for signing Up"
        total_price = request.data.get('total_price')
        name = request.data.get('name')
        if send_order_confirmation_email(order_id,name,email,order_items,total_price):
            return Response({"message":"email sent successfully!."})
class OrderCancelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self,request,order_id):
        try:
            order = Order.objects.get(order_id=order_id)
            if order.user != request.user:
                return Response({"error":"you are not authorized to cancel the order."},status=status.HTTP_403_FORBIDDEN)
            if order.status == "Cancelled":
                return Response({"message":" already oreder has cancelled!."},status=status.HTTP_200_OK)
            else: 
                order.status = "Cancelled"
                order.save()
                return Response({"message":"order cancelled successfully!."},status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error":"order not found!."},status=status.HTTP_400_BAD_REQUEST)       
#models.py
class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Restaurant(models.Model):
    name=models.CharField(max_length=30,blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    Mobile_number = models.CharField(max_length=15)
    opening_hours = models.JSONField(default=dict)
    logo = models.ImageField(upload_to="menu_items/",blank=True,null=True)
    operating_days = models.CharField(max_length=50,help_text = " eg: 'Mon,Tue,Wed,Thu,Fri'")
    def __str__(self):
        return f"{self.name},{self.mobile_number}" 
class Menuitem(models.Model):
    item_name = models.CharField(max_length=40)
    description = models.TextField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    image = models.ImageField(upload_to = 'menu_items/',blank=True,null=True)
    category = models.ForeignKey(MenuCategory,related_name="menu_item",on_delete=models.CASCADE)
    def __str__(self):
        return self.item_name
class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(required=True,unique=True)
    message = models.TextField(required=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}-{self.email}"
class Special(models.Model):
    item_name=models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    def __str__(self):
        return self.item_name
class Location(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=6)
    def __str__(self):
        return f"{self.address}"
class Order(models.Model):
    order_id = models.CharField(max_length=100,unique=True)
    user = models.ForeignKey(User,related_name="orders",on_delete=models.CASCADE)
    order_items = models.ManyToManyField(MenuItem,related_name="oredr_items")
    created_at=models.DateTimeField(auto_now_add=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    def save(self,*args,**kwargs):
        if not self.order_id:
            self.order_id = generate_unique_order_id(prefix="ORD")
        super().save(*args,**kwargs)
    def __str__(self):
        return self.order_id
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
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    feedback = models.TextField()
    def __str__(self):
        return self.name 
class Coupon(models.Model):
    code = models.CharField(max_length=25,unique=True)
    def __str__(self):
        return self.code
class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email
#home/serializers.py
class UserPrifileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name","email"]
class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ["name"]
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menuitem
        fields=["id","image","item_name","description","price","category"]
class OrdersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields =["order_id","user","order_items","created_at","total_price"]
class ContactFormSubmissionser(serializers.ModelSerializer):
    class Meta:
        model = ContactFormSubmission
        fields = ['name','email','message','submitted_at']
#forms.py
class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=["name","email","message"]
class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=150,widget=forms.Textinput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
#contextprocessors.py
def cart_items_count(request):
    cart = get_or_create_cart(request)
    return {"cart_item_count":cart.total_items}
#orders/models.py
class ActiveOrderManager(models.Manager):
    def get_active_orders(self):
        return self.filter(status__in = ["Pending","Processing"])
class Order(models.Model):
    STATUS_CHOICES = [('pending',"Pending"),
                    ("processing","Processing"),
                    ("shipped","Shipped"),
                    ("delivered","Delivered"),
                    ("cancelled","Cancelled"),]
    status = models.CharField(max_length=100,choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ActiveOrderManager()
#python shell
active_orders = Order.objects.get_active_orders()
print(active_orders)
#orders/utils.py
def generate_coupon_code(length:int=10,max_attempts:int=1000):
    alphabet = string.ascii_uppercase+string.digits 
    for attempt in range(max_attempts):
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        if not Coupon.objects.filter(code=code).exists():
            return code 

    raise ValueError("reach the attempts")
#utils/email.py
def send_order_confirmation_email(order_id,email,name,order_items,total_price):
    subject = f"order confirmation email for - {order_id}"
    item_list = "/n".join([f"{item}" for item in order_items])
    message = (f"Dear {name}\n
    Thank you for your order - {order_id}\n
    Items : {items_list}\n
    Total_Price:{total_price}.")
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, message, from_email, [email])
        logger.info(f"order conformation email sent to customer {email} for {order_id}")
        return {"status":"SUCCESS","message":"message sent successfully!."}
    except BadHeaderError:
        logger.error(f"Bad header error while sending email to {email}")
        return {"status":"error"}
    except Exception as e:
        logger.exception(f"failed send email to {email}")
        return {"message":"failed to send email"}
#orders/utils.py
def generate_unique_order_id(length=8,prefix=None):
    characters = string.ascii_uppercase+string.digits
    while True:
        random_part = ''.join(secrets.choice(characters) for _ in range(length))
        order_id = f"{slugify(prefix)}-{random_part}" if prefix else random_part
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id
#utils/validation_utils.py
logger = logging.get_logger(__name__)
def email_validation(email:str):
    if not email:
        return False
    try:
        result = validate_email(email,check_deliverability=False)
        normalized = result.email
        return True
    except EmailNotValidError as e:
        logger.warning("Invalid Email")
    except Exception as e:
        logger.error(f"error when validate email")
        return False"error during the email validation."
#urls.py
urlpatterns =[
    path("",views.home_view,name = "home_page"),
    path("menu/",views.menu_view,name="menu_items"),
    path("login/",views.login_view,name="login_view"),
    path("MenuAPI/",ListAPIView.as_view(),name= "menuAPI")
    # path("feedback/",views.feedback_view,name="feedback_form"),
]
def display_success_message():
    return "basic css styles added  successfully for the home page"  
if __name__ == "__main__":
    print(display_success_message())