from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'bill', views.TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', views.SummaryView.as_view())
]
