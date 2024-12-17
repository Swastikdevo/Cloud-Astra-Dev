from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.http import HttpResponse,JsonResponse
from .models import Borrower
from datetime import date
from twilio.rest import Client
import razorpay
from django.views.decorators.csrf import csrf_exempt




def members(request):
    payment_link = create_payment_link()
    today = date.today()
    target_date = today + timedelta(days=5)

    all_borrowers = Borrower.objects.all()
    complete = Borrower.objects.filter(payment_completed = True)
    near_due_borrowers = Borrower.objects.filter(
        repayment_last_date__lte=target_date,
        repayment_last_date__gte=today,payment_completed = False)
    


    context = {

        "all_borrowers": all_borrowers,
        "near_due_borrowers": near_due_borrowers,
        "complete":complete,
        
    }
    

    return render(request, "borrowers_dashboard.html", context)





@csrf_exempt
def webhook(request):
    borrower = Borrower.objects.get(phone_number='')
    borrower.payment_completed = True
    borrower.save()
    return JsonResponse({"status": "success", "message": "Payment updated successfully!"})




def ivr_response(request):
    audio_url = "https://file-examples.com/storage/fef4e75e176737761a179bf/2017/11/file_example_MP3_5MG.mp3"

    response_xml = f"""
    <Response>
        <Play>{audio_url}</Play>
        <GetDigits timeout="5" numDigits="1" action="http://127.0.0.1:8000/process-input">
            <PlayText>Please select an option. Press 1 for support. Press 2 for sales.</PlayText>
        </GetDigits>
    </Response>
    """
    return HttpResponse(response_xml, content_type="text/xml")

@csrf_exempt
def process_input(request):

    user_input = request.POST.get("Digits")
    if user_input == "1":
        response_xml = """
        <Response>
            <PlayText>Connecting you to support.</PlayText>
            <Dial>+919876543210</Dial>
        </Response>
        """
    elif user_input == "2":
        response_xml = """
        <Response>
            <PlayText>Connecting you to sales.</PlayText>
            <Dial>+919123456789</Dial>
        </Response>
        """
    else:
        response_xml = """
        <Response>
            <PlayText>Invalid input. Please try again.</PlayText>
        </Response>
        """
    return HttpResponse(response_xml, content_type="text/xml")

def stats(request):
    
    return render(request, "anna.html")














# import requests
# from requests.auth import HTTPBasicAuth

# EXOTEL_SID = "your_exotel_sid"
# EXOTEL_TOKEN = "your_exotel_token"
# CALLER_ID = "your_exotel_caller_id"

# def initiate_call(to_number):
#     """
#     Initiates an IVR call through Exotel.
#     """
#     api_url = f"https://api.exotel.com/v1/Accounts/{EXOTEL_SID}/Calls/connect"
#     payload = {
#         "From": to_number,
#         "To": "your_support_number",  # Example: your business number
#         "CallerId": CALLER_ID,
#         "Url": "http://your-server.com/ivr/ivr-response/"
#     }
#     response = requests.post(api_url, auth=HTTPBasicAuth(EXOTEL_SID, EXOTEL_TOKEN), data=payload)
#     return response.json()
