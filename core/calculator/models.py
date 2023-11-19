from django.db import models
from django.utils import timezone

from core.calculator.enums import MoneyEventType


class Client(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Loan(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Loan for {self.client.name} {self.client.surname}"


class MoneyEvent(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=2,
        choices=MoneyEventType.choices,
        default=MoneyEventType.INCREASE,
    )
    comment = models.TextField(blank=True)

    def __str__(self):
        return (
            f'{self.loan.client.name} {self.loan.client.surname}'
            f': {"-" if self.transaction_type == MoneyEventType.REPAYMENT else ""}{self.amount} EUR'
        )
