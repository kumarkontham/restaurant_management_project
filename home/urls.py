from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page,name="home_page"),
    path('about/',views.about_us,name='about_us'),
    path('menu/',views.menu_items_view,name='menu'),
]