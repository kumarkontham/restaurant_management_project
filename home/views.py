from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from .models import Restaurant
@api_view(['GET'])
def home_page(request):
    return render(request,'home/home.html')
# Create your views here.
