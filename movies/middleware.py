from django.contrib.auth.models import User
from django.shortcuts import redirect


class FirstRunRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not User.objects.exists():
            path = request.path
            if not (
                path.startswith("/admin/")
                or path.startswith("/static/")
                or path.startswith("/accounts/")
                or path.startswith("/register/")
                or path.startswith("/api/")
            ):
                return redirect("register")

        return self.get_response(request)
