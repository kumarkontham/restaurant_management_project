from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page,name="home_page"),
    path('about/',views.about_us,name='about_us'),
    path('menu/',views.hardcoded_items,name='menu'),
    path('feedback/',views.Feedback_view,name="feedback"),
    path('fedback/completed/',views.Feed)
]