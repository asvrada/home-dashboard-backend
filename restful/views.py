from rest_framework import viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum
from django.utils import timezone

from calendar import monthrange

from . import models
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class MonthlyBudgetView(generics.RetrieveUpdateAPIView):
    queryset = models.MonthlyBudget.objects.all()
    serializer_class = serializers.MonthlyBudgetSerializer

    def get_object(self):
        return self.queryset[0]


class SummaryView(APIView):
    def get(self, request):
        """
        Calculate the sum of income/spend this month
        1. 当日预算/共计
            budgetToday, budgetTodayTotal
        2. 当月预算/共计
            budgetMonth, budgetMonthTotal
        3. 当月预计存款
            savingMonth, incomeMonthTotal
        """
        # Get current date
        # Is this the same timezone as database?
        # Somehow we have to use local time to query, although the date stored in DB is in UTC
        # Maybe they get converted to local time before querying
        today = timezone.localdate()
        year, month, day = today.year, today.month, today.day

        bill_month = models.Transaction.objects.filter(time_created__year=year, time_created__month=month)
        bill_income_month = bill_month.filter(amount__gt=0)
        bill_spend_month = bill_month.filter(amount__lt=0)
        bill_today = bill_month.filter(time_created__day=day)

        # Sum of all income this month
        sum_income_month = self.aggregate_amount(bill_income_month)
        # Sum of all spending this month
        # A negative number
        sum_spend_month = self.aggregate_amount(bill_spend_month)
        # Sum of all spending today
        # A negative number
        sum_spend_today = self.aggregate_amount(bill_today.filter(amount__lte=0))

        # Days left for this month
        _, days_month = monthrange(year, month)
        # Days left, exclude today
        # Image its Jan, For 1st, there will 31days, for 31st, there will be 1 day
        # Also make sure its >= 1
        days_left = max(1, days_month - day + 1)

        # todo: set by user
        budget_month = 3333

        tmp_budget_month = budget_month + sum_spend_month
        tmp_budget_today_total = (tmp_budget_month - sum_spend_today) / days_left

        return Response(data={
            # budget left for today := budgetTodayTotal - spend today
            "budgetToday": tmp_budget_today_total + sum_spend_today,
            # budget today := (budgetMonth (not include today)) / days left
            "budgetTodayTotal": tmp_budget_today_total,
            # budget left for this month := budgetMonthTotal - total spend (include today)
            "budgetMonth": tmp_budget_month,
            # budget for this month := this is a number set by user
            "budgetMonthTotal": budget_month,
            # saving this month := total income - total spend
            "savingMonth": sum_income_month + sum_spend_month,
            # income this month := total income
            "incomeMonthTotal": sum_income_month,
        })

    @staticmethod
    def aggregate_amount(queryset):
        return queryset.aggregate(tmp_total=Sum('amount'))["tmp_total"] or 0

    @staticmethod
    def convert_float(number):
        return round(number)


class EnumViewSet(viewsets.ModelViewSet):
    queryset = models.EnumCategory.objects.all()
    serializer_class = serializers.EnumSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Transaction to be viewed or edited
    """
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
