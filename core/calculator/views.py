from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django.views.generic import TemplateView
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
    def loan_schedule(self, request, pk=None):
        loan = self.get_object()
        loan_schedule_items = calculate_loan_schedule(loan)
        serializer = LoanScheduleItemSerializer(loan_schedule_items, many=True)
        return Response(serializer.data)


class LoanView(TemplateView):
    template_name = "loan.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["loans"] = Loan.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
        data = [12, 19, 3, 5, 2, 3]
        return render(request, self.template_name, {"labels": labels, "data": data})


def home(request):
    loan_url = reverse("chart")  # 'chart' is the name of the LoanView route
    return HttpResponse(format_html("You're back home! <a href='{}'>Go to LoanView</a>", loan_url))
