from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': True,
            'status_code': response.status_code,
            'message': 'An error occurred.',
            'details': None
        }

        # Handling Validation Errors (400)
        if response.status_code == 400:
            custom_response_data['message'] = 'Validation failed.'
            custom_response_data['details'] = response.data

        # Handling Not Found (404)
        elif response.status_code == 404:
            custom_response_data['message'] = 'Resource not found.'
            
        # Handling Authentication/Authorization Errors (401, 403)
        elif response.status_code in [401, 403]:
            custom_response_data['message'] = response.data.get('detail', 'Authentication credentials were not provided or access is denied.')

        # For other standard errors, try to extract a 'detail' message if available
        else:
            if isinstance(response.data, dict) and 'detail' in response.data:
                 custom_response_data['message'] = response.data['detail']

        response.data = custom_response_data

    return response
