from django.contrib.auth import authenticate


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # authenticate user
        try:
            user = authenticate(request)
            if user is not None and user.is_authenticated:
                request.user = user
        except Exception as err:
            pass

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
