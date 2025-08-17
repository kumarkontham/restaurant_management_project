from django.db import models
from django.http import HttpResponse
from django import forms
from django.shortcuts import render,redirect
from django.urls import path
COPYRIGHT="\u00A9 | 2025 All Rights Reserved"
OPENING_HOURS = "Mon-Fri:9:00am-9:00pm,Sat-Sun:10:00am-10:00pm"
def home_page_rendering(title:str,body:str):
    html=f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <title>{title}</title>
    </head>
    <body>
    <header>
    <h2>Welcome to my Restaurant</h2>
    </header>
    <main>
    {body}
    </main>
    <footer>
    <small>Openings hours:{OPENING_HOURS}</small>
    <span>{COPYRIGHT}</span>
    </footer>
    </body>
    </html>
    """
    return HttpResponse(html)
def home_view(request):
    context="""<h2>welcome to my restaurant</h2><p>Enjoy the day!with our food.</p>
    <form method="get" action="#" class="search-bar">
    <input type="text" name="q" placeholder="search items">
    <button type="submit">Search</button>
    </form>"""
    return home_page_rendering("Home",context)
#models.py
class Feedback(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}-{self.comment}"
#forms.py
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows":4,"placeholder":"Enter your feedback."})
        }
#views.py
def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("feed_back_completed")
    else:
        form = FeedbackForm()
    return render(request,'home/feedback.html',{"form":form})
def feed_back_completed(request):
    return HttpResponse("<h2>Thank you for your response.</h2>")
#urls.py
urlpatterns =[
    path("feedback/",views.feedback_view,name="feedback_form"),
]
def display_success_message():
    return "basic css styles added  successfully for the home page"  
if __name__ == "__main__":
    print(display_success_message())