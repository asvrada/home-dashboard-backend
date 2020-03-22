from rest_framework import serializers
from .models import Transaction, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email']


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction
    """

    class Meta:
        model = Transaction
        fields = '__all__'
