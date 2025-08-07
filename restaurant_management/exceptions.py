from rest_framework.views import exception_handler
from rest_framework.response import Response 
from rest_framework import status
from django.http import Http404

def custom_exception_handler(exc,context):
    response= exception_handler(exc,context)
    if response is None and isinstance(exc,Http404):
        return Response({"error":"The request source not found","status":404},status=status.Http_404_NOT_FOUND)

    return response