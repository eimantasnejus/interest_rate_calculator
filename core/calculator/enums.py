from django.db.models import TextChoices


class MoneyEventType(TextChoices):
    INCREASE = "IN", "Increase"
    REPAYMENT = "RE", "Repayment"
