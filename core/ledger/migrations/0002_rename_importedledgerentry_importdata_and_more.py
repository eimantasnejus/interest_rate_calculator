# Generated by Django 4.2.7 on 2024-01-06 17:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ledger", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ImportedLedgerEntry",
            new_name="ImportData",
        ),
        migrations.RenameModel(
            old_name="LedgerEntrySubcategory",
            new_name="Subcategory",
        ),
        migrations.RenameField(
            model_name="ledgerentry",
            old_name="imported_ledger_entry",
            new_name="imported_entry",
        ),
    ]
