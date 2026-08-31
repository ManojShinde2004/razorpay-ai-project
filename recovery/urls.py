from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path(
        "recovery/",
        views.recovery,
        name="recovery"
    ),

    path(
        "analytics/",
        views.analytics,
        name="analytics"
    ),

    path(
        "analyze/<str:payment_id>/",
        views.analyze_payment,
        name="analyze_payment"
    ),

    path(
        "add-payment/",
        views.add_payment,
        name="add_payment"
    ),
]