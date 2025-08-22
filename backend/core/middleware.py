
from django.middleware.csrf import get_token

class EnsureCSRFMiddleware:
    """
        Add CSRF token in Cookie header Middleware
    """
    # middleware initial method
    def __init__(self, get_response):
        """
         get_response function for going to next ordered operation
        """
        self.get_response = get_response

    # middleware execution method
    def __call__(self, request):
        """
            Before get_response code executed before view or other middlewares
            After get_response code executed after view or other middlewares
        """
        response = self.get_response(request)

        if 'csrftoken' not in request.COOKIES:
            get_token(request)

        return response