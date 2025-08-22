import code

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST

def api_response(code=1 , message='success', data=None, status=HTTP_200_OK):
    return Response(
        {
            'code': code,
            'message': message,
            'data': data
        },
        status=status
    )

def api_success(code=1, message='operation successful', data=None, status=HTTP_200_OK):
    return api_response(code=code, message=message, data=data, status=status)

def api_error(code=0, message='operation failed', data=None, status=HTTP_400_BAD_REQUEST):
    return api_response(code=code, message=message, data=data, status=status)