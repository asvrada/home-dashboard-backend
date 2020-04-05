from rest_framework import serializers
from .models import Transaction, User, EnumCategory, MonthlyBudget, RecurringBill


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email']


class MonthlyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBudget
        fields = '__all__'


class EnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumCategory
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction
    """

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('time_created',)


class RecurringBillSerializer(serializers.ModelSerializer):
    """
    Serializer for RecurringBill
    """

    class Meta:
        model = RecurringBill
        fields = '__all__'
        read_only_fields = ('time_created',)
