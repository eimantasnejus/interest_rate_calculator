from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.calculator.helpers.loan_schedule_calculator import calculate_loan_schedule

from .models import Loan
from .serializers import LoanScheduleItemSerializer, LoanSerializer


class LoanViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    @action(detail=True, serializer_class=LoanScheduleItemSerializer)
    def loan_schedule(self, request):
        loan = self.get_object()
        loan_schedule_items = calculate_loan_schedule(loan)
        serializer = LoanScheduleItemSerializer(loan_schedule_items, many=True)
        return Response(serializer.data)
