from datetime import datetime
def generate_footer(notice:str = "All Rights Reserved!."):
    curr_year = datetime.now().year 
    return f'&copy; {curr_year}|{notice}'
def reservation_message(place_holder:str="reservation page is under construction!. Reservation features available soon."):
    return f'{place_holder}'
def display_success_message():
    return "basic css styles added  successfully for the home page"
def retrive_contact():
    return "+91-8976543245"
if __name__ == "__main__":
    print(display_success_message())


