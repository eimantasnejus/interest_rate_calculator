from django.db import models

from core.ledger.enums import DebitCredit, EntryCategory, ImportedFrom


class Account(models.Model):
    name = models.CharField(max_length=100)
    iban = models.CharField(max_length=34, unique=True)

    def __str__(self):
        return f"{self.name} - {self.iban[-4:]}"


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=EntryCategory.choices, default=EntryCategory.OTHER)

    def __str__(self):
        return f"{self.category}/{self.name}"


class ImportData(models.Model):
    account_iban = models.CharField(max_length=34, blank=True)
    imported_from = models.CharField(max_length=100, choices=ImportedFrom.choices, default=ImportedFrom.SWEDBANK)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    transaction_code = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    beneficiary = models.CharField(max_length=200, blank=True)
    details = models.CharField(max_length=400, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    currency = models.CharField(max_length=3, default="EUR", blank=True)
    type = models.CharField(max_length=1, choices=DebitCredit.choices, blank=True)
    record_id = models.BigIntegerField(null=True, blank=True)
    code = models.CharField(max_length=100, blank=True)
    reference_no = models.CharField(max_length=100, blank=True)
    doc_nr = models.CharField(max_length=100, blank=True)
    code_in_payer_is = models.CharField(max_length=100, blank=True)
    client_code = models.CharField(max_length=100, blank=True)
    originator = models.CharField(max_length=100, blank=True)
    beneficiary_party = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{"+" if self.type == DebitCredit.DEBIT else "-"}{self.amount} - {self.beneficiary}'

    def to_ledger_entry(self):
        # Skip the record with id 1111, which indicates that this is closing / opening balance or turnover.
        if self.record_id == 1111:
            return
        # Avoid duplicates.
        if LedgerEntry.objects.filter(imported_ledger_entry=self).exists():
            return
        account, _ = Account.objects.get_or_create(iban=self.account_iban, defaults={"name": "Unknown"})
        return LedgerEntry.objects.create(
            account=account,
            date=self.date,
            beneficiary=self.beneficiary if self.beneficiary else "SWEDBANK",
            details=self.details,
            amount=self.amount,
            currency=self.currency,
            type=self.type,
            record_id=self.record_id,
            code=self.code,
            imported_ledger_entry=self,
            subcategory=None,
        )


class LedgerEntry(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()
    beneficiary = models.CharField(max_length=200)
    details = models.CharField(max_length=400)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")
    type = models.CharField(max_length=1, choices=DebitCredit.choices)
    record_id = models.BigIntegerField(null=True)
    code = models.CharField(max_length=100, blank=True)
    imported_entry = models.ForeignKey(ImportData, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    cancels_out = models.ForeignKey(
        "LedgerEntry",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="If this entry cancels out another entry, select the other entry here.",
    )
    is_recurring = models.BooleanField(default=False)
    non_standard_category = models.BooleanField(default=False)

    def __str__(self):
        return f'{"+" if self.type == DebitCredit.DEBIT else "-"}{self.amount}: ({self.id})'

    def categorise_automatically(self):
        if self.subcategory:
            return
        similar_categorised_ledger_entry = (
            LedgerEntry.objects.filter(beneficiary=self.beneficiary)
            .exclude(subcategory=None, non_standard_category=True)
            .first()
        )
        if similar_categorised_ledger_entry:
            self.subcategory = similar_categorised_ledger_entry.subcategory
            self.save()
