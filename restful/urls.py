from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'bill', views.TransactionViewSet, basename="bill")
router.register(r'enum', views.EnumViewSet, basename="enum")

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', views.SummaryView.as_view(), name="get"),
    path('budget/', views.MonthlyBudgetView.as_view(), name="budget")
]
