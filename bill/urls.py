from django.urls import path, include
from rest_framework.routers import DefaultRouter
from graphene_django.views import GraphQLView

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'bill', views.TransactionViewSet, basename="bill")
router.register(r'recurring_bill', views.RecurringBillViewSet, basename="recurring_bill")
router.register(r'enum', views.EnumViewSet, basename="enum")

urlpatterns = [
    path('', include(router.urls)),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path('summary/', views.SummaryView.as_view(), name="summary"),
    path('budget/', views.MonthlyBudgetView.as_view(), name="budget"),
]
