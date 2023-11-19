from django.contrib import admin

from .models import Client, Loan, MoneyEvent

admin.site.register(Client)
admin.site.register(Loan)


@admin.register(MoneyEvent)
class MoneyEventAdmin(admin.ModelAdmin):
    list_display = ("__str__", "date", "amount", "transaction_type")
