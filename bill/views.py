from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum, Max
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
        assert len(self.queryset.all()) >= 1, "No record in Budget database! Create one on admin site."
        return self.queryset.first()


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
        4. 当月固定开销
            monthlyCost
        """
        # Get current date
        # Is this the same timezone as database?
        # Somehow we have to use local time to query, although the date stored in DB is in UTC
        # Maybe they get converted to local time before querying
        today = timezone.localdate()
        year, month, day = today.year, today.month, today.day

        bill_month = models.Transaction.objects.filter(time_created__year=year, time_created__month=month)
        bill_spend_month = bill_month.filter(amount__lt=0)
        bill_today = bill_month.filter(time_created__day=day)

        last_year = year
        last_month = month - 1
        if last_month == 0:
            last_month = 12
            last_year -= 1
        bill_income_last_month = models.Transaction.objects.filter(time_created__year=last_year,
                                                                   time_created__month=last_month, amount__gt=0)
        sum_income_last_month = self.aggregate_amount(bill_income_last_month)

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

        budget_month = self.retrieve_budget()

        tmp_budget_month = budget_month + sum_spend_month
        tmp_budget_today_total = (tmp_budget_month - sum_spend_today) / days_left

        monthly_cost = self.get_recurring_cost_each_month()

        return Response(data={
            # budget left for today := budgetTodayTotal - spend today
            "budgetToday": self.convert_float(tmp_budget_today_total + sum_spend_today),
            # budget today := (budgetMonth (not include today)) / days left
            "budgetTodayTotal": self.convert_float(tmp_budget_today_total),

            # budget left for this month := budgetMonthTotal - total spend (include today)
            "budgetMonth": self.convert_float(tmp_budget_month),
            # budget for this month := this is a number set by user
            "budgetMonthTotal": self.convert_float(budget_month),

            # saving this month := total income - total spend
            "savingMonth": self.convert_float(sum_income_last_month + sum_spend_month),
            # income this month := total income from last month
            "incomeMonthTotal": self.convert_float(sum_income_last_month),

            "monthlyCost": self.convert_float(monthly_cost)
        })

    @staticmethod
    def retrieve_budget():
        if models.MonthlyBudget.objects.filter(pk=1).count() != 1:
            raise Exception("MonthlyBudget record count != 1")

        return models.MonthlyBudget.objects.get(pk=1).budget

    @staticmethod
    def aggregate_amount(queryset):
        return queryset.aggregate(tmp_total=Sum('amount'))["tmp_total"] or 0

    @staticmethod
    def convert_float(number):
        return round(number)

    @staticmethod
    def get_recurring_cost_each_month():
        rb_all = models.RecurringBill.objects.all()
        rb_monthly = rb_all.filter(frequency='M')
        rb_yearly = rb_all.filter(frequency='Y')

        sum_monthly = rb_monthly.aggregate(tmp_result=Sum('amount'))["tmp_result"] or 0
        sum_year = rb_yearly.aggregate(tmp_result=Sum('amount'))["tmp_result"] or 0

        return sum_monthly + sum_year / 12


class IconViewSet(viewsets.ModelViewSet):
    queryset = models.Icon.objects.all()
    serializer_class = serializers.IconSerializer


class EnumViewSet(viewsets.ModelViewSet):
    queryset = models.EnumCategory.objects.all()
    serializer_class = serializers.EnumSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Transaction to be viewed or edited
    """
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer


class RecurringBillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Recurring Bill to be viewed or edited
    """
    queryset = models.RecurringBill.objects.all()
    serializer_class = serializers.RecurringBillSerializer
