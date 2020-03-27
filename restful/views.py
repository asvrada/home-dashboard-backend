from rest_framework import viewsets
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


class SummaryView(APIView):
    def get(self, request):
        """
        Calculate the sum of income/spend this month
        total: sum of income this month
        budgetTotal: budget left for this month
        budgetToday: budget left for today
        """
        # Get current date
        today = timezone.now()
        year, month, day = today.year, today.month, today.day

        bill_month = models.Transaction.objects.filter(time_created__year=year, time_created__month=month)
        bill_income_month = bill_month.filter(amount__gte=0)
        bill_today = bill_month.filter(time_created__day=day)

        # Sum of all income this month
        sum_income_month = self.aggregate_amount(bill_income_month)
        # Sum of all spending this month
        # A negative number
        sum_this_month = self.aggregate_amount(bill_month.filter(amount__lte=0))
        # Sum of all spending today
        # A negative number
        sum_today = self.aggregate_amount(bill_today.filter(amount__lte=0))

        # Days left for this month
        _, days_month = monthrange(year, month)
        # Days left, exclude today
        # Image its Jan, For 1st, there will 31days, for 31st, there will be 1 day
        # Also make sure its >= 1
        days_left = max(1, days_month - day + 1)

        return Response(data={
            "total": self.convert_float(sum_income_month),
            "budgetTotal": self.convert_float(sum_income_month + sum_this_month),
            "budgetToday": self.convert_float((sum_income_month + sum_this_month - sum_today) / days_left)
        })

    @staticmethod
    def aggregate_amount(queryset):
        return queryset.aggregate(tmp_total=Sum('amount'))["tmp_total"] or 0

    @staticmethod
    def convert_float(number):
        return round(number)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Transaction to be viewed or edited
    """
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
