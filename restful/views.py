from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
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
        return Response(data={
            "total": 7000,
            "remainingTotal": 1200,
            "remainingToday": 200
        })


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Transaction to be viewed or edited
    """
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
