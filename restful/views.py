from calendar import monthrange

from django.db.models import Sum, F
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from backend import exceptions, models
from . import serializers
from .google_oauth import get_google_user_from_google_token


def get_jwt_token(user):
    refresh_token_obj = RefreshToken.for_user(user)

    refresh = str(refresh_token_obj)
    access = str(refresh_token_obj.access_token)

    return access, refresh


class UserView(generics.RetrieveAPIView):
    """
    Retrieve the current user
    """
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class GoogleLogin(APIView):
    permission_classes = []

    def post(self, request):
        token = request.data.get("token", None)

        if token is None:
            return Response(status=400, data={"error": "Please provide Google access token in POST body"})

        google_user_object = get_google_user_from_google_token(token)

        user = self.get_or_create_user_given_google_user_object(google_user_object)

        # return user's access and refresh token
        access, refresh = get_jwt_token(user)

        return Response(data={
            "access": access,
            "refresh": refresh
        })

    @staticmethod
    def get_or_create_user_given_google_user_object(google_user_object):
        google_user_id = google_user_object["sub"]

        users = models.User.objects.filter(google_user_id=google_user_id)

        if users.count() > 1:
            raise exceptions.ImpossibleException(f"More than 1 result given google user id: {google_user_id}")

        if users.count() == 0:
            # create user
            user = models.User.objects.create_user(email=google_user_object["email"],
                                                   username=google_user_object["name"],
                                                   password="default",
                                                   first_name=google_user_object["given_name"],
                                                   last_name=google_user_object["family_name"],
                                                   google_user_id=google_user_id)
            user.budget = models.MonthlyBudget.objects.create(budget=2000)
            user.save()
        else:
            user = users.first()

        return user


class MonthlyBudgetView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.MonthlyBudgetSerializer

    def get_object(self):
        return self.get_queryset()

    def get_queryset(self):
        return self.request.user.budget


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
        user = request.user

        if not user.is_authenticated:
            return Response(status=401)

        bill_current_user = user.bills

        # Get current date
        # Is this the same timezone as database?
        # Somehow we have to use local time to query, although the date stored in DB is in UTC
        # Maybe they get converted to local time before querying
        today = timezone.localdate()
        year, month, day = today.year, today.month, today.day

        bill_month = bill_current_user.filter(time_created__year=year, time_created__month=month)
        bill_spend_month = bill_month.filter(amount__lt=0)
        bill_today = bill_month.filter(time_created__day=day)

        last_year = year
        last_month = month - 1
        if last_month == 0:
            last_month = 12
            last_year -= 1
        bill_income_last_month = bill_current_user.filter(time_created__year=last_year,
                                                          time_created__month=last_month, amount__gt=0)
        sum_income_last_month = self.aggregate_amount(bill_income_last_month)

        # Sum of all spending this month, exclude marked as skip total
        # Note: a negative number
        sum_spend_month = self.aggregate_amount(
            bill_spend_month
                .annotate(flag=F('skip_summary_flag').bitand(models.FLAG_SKIP_TOTAL))
                .exclude(flag=models.FLAG_SKIP_TOTAL)
        )
        # Sum of all spending this month, exclude these marked as skip budget
        # Note: a negative number
        sum_spend_month_skipped = self.aggregate_amount(
            bill_spend_month
                .annotate(flag=F('skip_summary_flag').bitand(models.FLAG_SKIP_BUDGET))
                .exclude(flag=models.FLAG_SKIP_BUDGET)
        )
        # Sum of all spending today, exclude these marked as skip budget
        # Note: a negative number
        sum_spend_today = self.aggregate_amount(
            bill_today
                # negative amount will pass
                .filter(amount__lte=0)
                # not marked skip budget will pass
                .annotate(flag=F('skip_summary_flag').bitand(models.FLAG_SKIP_BUDGET))
                .exclude(flag=models.FLAG_SKIP_BUDGET)
        )

        # Days left for this month
        _, days_month = monthrange(year, month)
        # Days left, exclude today
        # Image its Jan, For 1st, there will 31days, for 31st, there will be 1 day
        # Also make sure its >= 1
        days_left = max(1, days_month - day + 1)

        budget_month = self.retrieve_budget(user)

        tmp_budget_month = budget_month + sum_spend_month_skipped
        tmp_budget_today_total = (tmp_budget_month - sum_spend_today) / days_left

        monthly_cost = self.get_recurring_cost_each_month(user)

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

            "monthlyCost": round(monthly_cost, 2)
        })

    @staticmethod
    def retrieve_budget(user):
        return user.budget.budget

    @staticmethod
    def aggregate_amount(queryset):
        return queryset.aggregate(tmp_total=Sum('amount'))["tmp_total"] or 0

    @staticmethod
    def convert_float(number):
        return round(number)

    @staticmethod
    def get_recurring_cost_each_month(user):
        """
        Sum of all recurring bill
        """
        rb_all = user.rbs
        rb_monthly = rb_all.filter(frequency='M')
        rb_yearly = rb_all.filter(frequency='Y')

        sum_monthly = rb_monthly.aggregate(tmp_result=Sum('amount'))["tmp_result"] or 0
        sum_year = rb_yearly.aggregate(tmp_result=Sum('amount'))["tmp_result"] or 0

        return sum_monthly + sum_year / 12
