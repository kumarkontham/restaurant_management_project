import json
from datetime import datetime
def error_handling():
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
        print(json.dumps({"status"=500,"error":str(e)}))


