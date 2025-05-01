# utils/exception_handlers.py
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        customized_response = {
            'error': {
                'code': response.status_code,
                'message': response.data.get('detail', 'Request failed'),
                'details': response.data
            }
        }
        response.data = customized_response
    
    return response