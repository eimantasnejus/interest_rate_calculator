from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from rest_framework import routers

from core.calculator.views import LoanViewSet, LoanView, home

router = routers.DefaultRouter()
router.register(r"loans", LoanViewSet, basename="loans")

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy('home')), name="index"),
    path("home/", home, name="home"),
    path("loan/", LoanView.as_view(), name="chart"),
]
