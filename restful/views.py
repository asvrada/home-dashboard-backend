from rest_framework import viewsets
from . import models
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Transaction to be viewed or edited
    """
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
