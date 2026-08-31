from django.db import models


class Payment(models.Model):

    payment_id = models.CharField(
        max_length=50,
        unique=True
    )

    customer = models.CharField(
        max_length=100
    )

    amount = models.IntegerField()

    status = models.CharField(
        max_length=20
    )

    reason = models.CharField(
        max_length=100,
        blank=True
    )

    # ML features
    previous_failures = models.IntegerField(
        default=0
    )

    customer_history = models.IntegerField(
        default=1
    )

    payment_method = models.CharField(
        max_length=30,
        default="UPI"
    )

    retry_count = models.IntegerField(
        default=0
    )

    customer_age_days = models.IntegerField(
        default=365
    )

    # AI output
    recovery_probability = models.IntegerField(
        default=0
    )

    recommended_action = models.CharField(
        max_length=200,
        blank=True
    )

    # Whether the failed payment was eventually recovered
    recovered = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.payment_id