from django.urls import path

from . import views

urlpatterns = [
    path('summary/', views.SummaryView.as_view(), name="summary"),
    path('budget/', views.MonthlyBudgetView.as_view(), name="budget"),
]
