from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from django.conf import settings
from restful.views import GoogleLogin

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth
    path('google-login/', GoogleLogin.as_view(), name="google_login"),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Endpoint for applications
    path('restful/', include('restful.urls')),
    path('', include('graphqlapi.urls')),

]

if settings.DEBUG:
    urlpatterns += [
        path('email-login/', TokenObtainPairView.as_view(), name='email_login'),
    ]
