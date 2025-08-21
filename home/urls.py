from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page,name="home_page"),
    path('about/',views.about_us,name='about_us'),
    path('menu/',views.hardcoded_items,name='menu'),
    path('feedback/',views.feedback_view,name="feedback"),
    path('fedback/completed/',views.feedback_thanks_view,name="feedback_completed"),
    path('menu/',views.MenuAPIView.as_view(),name="menu_items")
]