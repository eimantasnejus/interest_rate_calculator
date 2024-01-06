from django.db.models import TextChoices


class DebitCredit(TextChoices):
    """Debit or Credit."""

    DEBIT = "D", "Debit"
    CREDIT = "K", "Credit"


class ImportedFrom(TextChoices):
    """Where was the ledger entry imported from."""

    SWEDBANK = "SWEDBANK", "Swedbank"


class EntryCategory(TextChoices):
    """Entry category."""

    LIFE_AND_ENTERTAINMENT = "life_and_entertainment", "Life and entertainment"
    HOME = "home", "Home"
    INCOME = "income", "Income"
    TRANSPORT = "transport", "Transport"
    FOOD_AND_DRINK = "food_and_drink", "Food and drink"
    HEALTH_AND_EDUCATION = "health_and_education", "Health and education"
    SHOPPING = "shopping", "Shopping"
    PETS = "pets", "Pets"
    INVESTMENTS = "investments", "Investments"
    FINANCIAL_EXPENSES = "financial_expenses", "Financial expenses"
    OTHER = "other", "Other"
