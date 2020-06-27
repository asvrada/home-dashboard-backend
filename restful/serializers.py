from rest_framework import serializers

from backend.models import User, MonthlyBudget


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'has_password', 'google_user_id']


class MonthlyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBudget
        fields = ('budget',)
