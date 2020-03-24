from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum

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
        remainingTotal: {total} - sum of spend this month
        remainingToday: ({total} - sum of spend (except today)) / days till end of month
        """
        total_amount = models.Transaction.objects.all().aggregate(tmp_total=Sum('amount'))["tmp_total"]

        return Response(data={
            "total": total_amount,
            "remainingTotal": 1200,
            "remainingToday": 200
        })


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Transaction to be viewed or edited
    """
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
