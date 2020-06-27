from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.UserView.as_view(), name="user"),
    path('summary/', views.SummaryView.as_view(), name="summary"),
    path('budget/', views.MonthlyBudgetView.as_view(), name="budget"),
]
