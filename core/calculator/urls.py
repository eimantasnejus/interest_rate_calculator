from rest_framework import routers

from core.calculator.views import LoanViewSet

router = routers.DefaultRouter()
router.register(r"loans", LoanViewSet, basename="loans")
