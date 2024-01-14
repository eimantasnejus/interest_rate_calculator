from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.resources import ModelResource

from core.ledger.models import Account, ImportData, LedgerEntry, Subcategory

admin.site.register(Account)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category")
    list_filter = ("category",)
    search_fields = ("name", "category")


class ImportDataResource(ModelResource):
    account_iban = Field(attribute="account_iban", column_name="Account No")
    date = Field(attribute="date", column_name="Date")
    beneficiary = Field(attribute="beneficiary", column_name="Beneficiary")
    details = Field(attribute="details", column_name="Details")
    amount = Field(attribute="amount", column_name="Amount")
    currency = Field(attribute="currency", column_name="Currency")
    type = Field(attribute="type", column_name="D/K")
    record_id = Field(attribute="record_id", column_name="Record ID")
    code = Field(attribute="code", column_name="Code")
    reference_no = Field(attribute="reference_no", column_name="Reference No")
    doc_nr = Field(attribute="doc_nr", column_name="Doc No")
    code_in_payer_is = Field(attribute="code_in_payer_is", column_name="Code in payer IS")
    client_code = Field(attribute="client_code", column_name="Client code")
    originator = Field(attribute="originator", column_name="Originator")
    beneficiary_party = Field(attribute="beneficiary_party", column_name="Beneficiary party")

    class Meta:
        model = ImportData
        fields = "__all__"
        import_id_fields = ["account_iban", "date", "beneficiary", "details", "amount", "type"]
        use_bulk = True
        skip_unchanged = True

    def before_import_row(self, row, **kwargs):
        # Invert the D/K column. I suppose CSV is made from bank's perspective, but we want to see it from ours.
        row["D/K"] = "K" if row["D/K"] == "D" else "D"
        # Apply the default value for Record ID, as it can be empty in the CSV.
        row["Record ID"] = 1111 if not row["Record ID"] else row["Record ID"]


@admin.register(ImportData)
class ImportDataAdmin(ImportExportModelAdmin):
    resource_class = ImportDataResource
    search_fields = ("account_iban", "beneficiary", "details", "amount")
    list_display = (
        "__str__",
        "date",
        "account",
        "beneficiary",
        "details",
        "amount",
        "type",
        "record_id",
    )
    actions = ["convert_to_ledger_entries"]

    def convert_to_ledger_entries(self, request, queryset):
        for imported_ledger_entry in queryset:
            imported_ledger_entry.to_ledger_entry()


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "date",
        "subcategory",
        "account",
        "beneficiary",
        "details",
        "amount",
        "type",
    )
    list_filter = ("account", "type", "date", "type", "beneficiary")
    search_fields = ("account__name", "beneficiary", "details", "amount")
    actions = ["categorise_automatically"]
    autocomplete_fields = ["cancels_out", "subcategory"]
    readonly_fields = ["imported_entry"]

    def categorise_automatically(self, request, queryset):
        for ledger_entry in queryset:
            ledger_entry.categorise_automatically()
