from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth
    path('token-auth/', TokenObtainPairView.as_view(), name='token_auth'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Endpoint for applications
    path('restful/', include('restful.urls')),
    path('', include('graphqlapi.urls')),

    # path('google-login/')
    # path('google-signup/')
]
