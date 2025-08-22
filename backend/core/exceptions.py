from rest_framework.views import exception_handler
from .response import api_error
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        message = response.data.get('detail', str(exc))
        return api_error(message=message, status=response.status_code)

    return api_error(message="Internal server error", status=HTTP_500_INTERNAL_SERVER_ERROR)