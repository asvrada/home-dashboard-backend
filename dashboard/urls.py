"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from bill.views import PrivateGraphQLView, TestGraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),

    # bill application
    path('bill/', include('bill.urls')),
    path('graphql/', PrivateGraphQLView.as_view()),

    path('token-auth/', TokenObtainPairView.as_view(), name='token_auth'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    urlpatterns += [
        path('graphqltest/', TestGraphQLView.as_view(graphiql=True)),
        path('graphqltest/<str:username>', TestGraphQLView.as_view(graphiql=True)),
    ]
