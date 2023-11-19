from rest_framework import serializers

from core.calculator.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["client", "amount", "interest_rate", "start_date"]


class LoanScheduleItemSerializer(serializers.Serializer):
    date = serializers.DateField()
    days_from_last_item = serializers.IntegerField()
    daily_interest_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    last_period_accrued_interest = serializers.DecimalField(max_digits=10, decimal_places=2)
    change_in_outstanding_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    outstanding_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
