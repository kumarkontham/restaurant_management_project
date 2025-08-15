import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
CONTACT_HTML ="""
<!DOCTYPE html>
<html>
<head>
<title>Contact us</title>
<script>
function ValidateContactForm(){
    let name = document.forms["ContactForm"]["name"].value.trim()
    let email = document.forms["ContactForm"]["email"].value.trim()
    if (name=="" || email ==""){
        window.alert("provide both name and email to proceed")
        return false;
    }
    return true;
}
</script>
</head>
<body>
    <h2>Contact Form</h2>
    <form name="ContactForm" method="POST" onsubmit="return ValidateContactForm()">
        <input type="text" name="name" placeholder="Enter name"><br><br>
        <input type="text" name="email" placeholder="enter email"><br>
        <textarea name="message"></textarea>
        <button type="submit">send</button>
    </form>
</body>
</html>
"""
@csrf_exempt
def contact_view(request):
    if request.method =="POST":
        return HttpResponse("<h1>message received</h1>",content_type="text/html")
    return HttpResponse(CONTACT_HTML,content_type="text/html")
#urls.py 
urlpatterns=[
    path("contact/",main.contact_view,name="contact")
]

def error_handling():
    """in the  process of retriving the data occur any errors like database errors and object not found errors and any unexpected errors occurred display the messages in Json format"""
    try:
        from django.http import JsonResponse
        from django.db import DatabaseError
        from django.apps import apps
        Restaurant = apps.get_model(app_label='restaurant',model_name='Restaurant')
        restaurant =  Restaurant.objects.first()
        if restaurant is None:
            return JsonResponse({"error":"No restaurant found in the database!."},status=404)
        else:
            return JsonResponse({"name": restaurant.name })
    except DatabaseError:
        return JsonResponse({"error":"A database error occurred!. please try again later."},status=500)
    except Exception as e:
        return JsonResponse({"error":f"An unexpected error occured!.{str(e)}"},status=500)
def generate_footer(notice:str = "All Rights Reserved!."):
    curr_year = datetime.now().year 
    return f'&copy; {curr_year}|{notice}'
def reservation_message(place_holder:str = "reservation page is under construction!. Reservation features available soon."):
    return f'{place_holder}'
def display_success_message():
    return "basic css styles added  successfully for the home page"
def retrieve_contact():
    return "+91-8976543245"
if __name__ == "__main__":
    try:
        print(error_handling())
    except Exception as e:
        print(json.dumps({"status":500,"error":str(e)}))


