from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment

import joblib
import os
import pandas as pd

from django.conf import settings
from datetime import datetime


# ============================================================
# LOAD TRAINED AI MODEL
# ============================================================

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "ml",
    "recovery_model.pkl"
)

model = joblib.load(MODEL_PATH)


# ============================================================
# DASHBOARD
# ============================================================

def dashboard(request):

    payments = Payment.objects.all().order_by("-id")

    total_payments = payments.count()

    failed_payments = payments.filter(
        status__iexact="Failed"
    ).count()

    successful_payments = payments.filter(
        status__iexact="Success"
    ).count()

    recovered_payments = payments.filter(
        recovered=True
    ).count()

    total_amount = sum(
        float(payment.amount)
        for payment in payments
    )

    context = {
        "payments": payments,
        "total": total_payments,
        "failed": failed_payments,
        "successful": successful_payments,
        "recovered": recovered_payments,
        "total_amount": total_amount,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


# ============================================================
# RECOVERY PAGE
# ============================================================

def recovery(request):

    payments = Payment.objects.filter(
        status__iexact="Failed"
    ).order_by("-id")

    total_failed = payments.count()

    failed_amount = sum(
        float(payment.amount)
        for payment in payments
    )

    context = {
        "payments": payments,
        "total_failed": total_failed,
        "failed_amount": failed_amount,
    }

    return render(
        request,
        "recovery.html",
        context
    )


# ============================================================
# ANALYZE PAYMENT USING AI
# ============================================================

def analyze_payment(request, payment_id):

    payment = get_object_or_404(
        Payment,
        payment_id=payment_id
    )

    # --------------------------------------------------------
    # BASIC PAYMENT INFORMATION
    # --------------------------------------------------------

    amount = float(payment.amount)

    previous_failures = getattr(
        payment,
        "previous_failures",
        0
    )

    customer_history = getattr(
        payment,
        "customer_history",
        1
    )

    failure_reason = getattr(
        payment,
        "reason",
        "unknown"
    )

    payment_method = getattr(
        payment,
        "payment_method",
        "UPI"
    )

    retry_count = getattr(
        payment,
        "retry_count",
        0
    )

    customer_age_days = getattr(
        payment,
        "customer_age_days",
        365
    )

    # --------------------------------------------------------
    # TIME INFORMATION
    # --------------------------------------------------------

    time_of_day = datetime.now().hour

    day_type = (
        "weekday"
        if datetime.now().weekday() < 5
        else "weekend"
    )

    # --------------------------------------------------------
    # CREATE INPUT DATA
    #
    # These MUST match the features used while training.
    # --------------------------------------------------------

    input_data = pd.DataFrame([{

        "amount": amount,

        "previous_failures": previous_failures,

        "customer_history": customer_history,

        "failure_reason": failure_reason,

        "payment_method": payment_method,

        "retry_count": retry_count,

        "customer_age_days": customer_age_days,

        "time_of_day": time_of_day,

        "day_type": day_type,

    }])

    # --------------------------------------------------------
    # AI PREDICTION
    # --------------------------------------------------------

    probability = model.predict_proba(
        input_data
    )[0][1]

    probability_percentage = round(
        probability * 100,
        2
    )

    # --------------------------------------------------------
    # RECOVERY RECOMMENDATION
    # --------------------------------------------------------

    reason = str(
        failure_reason
    ).lower()

    if reason == "insufficient_funds":

        recommendation = (
            "Ask customer to add funds or use "
            "an alternate payment method"
        )

    elif reason == "expired_card":

        recommendation = (
            "Ask customer to update the card "
            "or use another payment method"
        )

    elif reason in [
        "network_error",
        "timeout",
        "bank_server_error"
    ]:

        recommendation = "Retry Payment"

    elif reason == "transaction_limit":

        recommendation = (
            "Use an alternate payment method "
            "or retry later"
        )

    elif reason == "customer_cancelled":

        recommendation = "Send Payment Reminder"

    elif reason == "risk_declined":

        recommendation = (
            "Request verification or use "
            "an alternate payment method"
        )

    elif reason == "authentication_failed":

        recommendation = (
            "Ask customer to retry authentication"
        )

    else:

        if probability_percentage >= 70:

            recommendation = "Retry Payment"

        elif probability_percentage >= 40:

            recommendation = "Send Payment Reminder"

        else:

            recommendation = (
                "Use Alternate Payment Method"
            )

    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    context = {

        "payment": payment,

        "probability": probability_percentage,

        "recommendation": recommendation,

        "previous_failures": previous_failures,

        "customer_history": customer_history,

    }

    return render(
        request,
        "analysis.html",
        context
    )


# ============================================================
# ADD PAYMENT
# ============================================================

def add_payment(request):

    if request.method == "POST":

        payment_id = request.POST.get(
            "payment_id"
        )

        customer = request.POST.get(
            "customer"
        )

        amount = request.POST.get(
            "amount"
        )

        status = request.POST.get(
            "status"
        )

        reason = request.POST.get(
            "reason"
        )

        Payment.objects.create(

            payment_id=payment_id,

            customer=customer,

            amount=amount,

            status=status,

            reason=reason,

        )

        return redirect("/")

    return render(
        request,
        "add_payment.html"
    )


# ============================================================
# ANALYTICS
# ============================================================

def analytics(request):

    payments = Payment.objects.all()

    # --------------------------------------------------------
    # COUNTS
    # --------------------------------------------------------

    total_payments = payments.count()

    failed_payments = payments.filter(
        status__iexact="Failed"
    ).count()

    successful_payments = payments.filter(
        status__iexact="Success"
    ).count()

    recovered_payments = payments.filter(
        recovered=True
    ).count()

    # --------------------------------------------------------
    # AMOUNTS
    # --------------------------------------------------------

    total_amount = sum(
        float(payment.amount)
        for payment in payments
    )

    success_amount = sum(
        float(payment.amount)
        for payment in payments.filter(
            status__iexact="Success"
        )
    )

    failed_amount = sum(
        float(payment.amount)
        for payment in payments.filter(
            status__iexact="Failed"
        )
    )

    # --------------------------------------------------------
    # RECOVERY RATE
    # --------------------------------------------------------

    if failed_payments > 0:

        recovery_rate = round(
            (
                recovered_payments /
                failed_payments
            ) * 100,
            1
        )

    else:

        recovery_rate = 0

    # --------------------------------------------------------
    # ESTIMATED RECOVERY
    # --------------------------------------------------------

    if failed_payments > 0:

        estimated_recovery = round(
            failed_amount *
            (
                recovered_payments /
                failed_payments
            ),
            2
        )

    else:

        estimated_recovery = 0

    # --------------------------------------------------------
    # CHART DATA
    # --------------------------------------------------------

    status_labels = [
        "Successful",
        "Failed"
    ]

    status_counts = [
        successful_payments,
        failed_payments
    ]

    value_labels = [
        "Successful",
        "Failed"
    ]

    value_amounts = [
        success_amount,
        failed_amount
    ]

    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    context = {

        "total": total_payments,

        "failed": failed_payments,

        "successful": successful_payments,

        "recovered": recovered_payments,

        "total_amount": total_amount,

        "success_amount": success_amount,

        "failed_amount": failed_amount,

        "recovery_rate": recovery_rate,

        "estimated_recovery": estimated_recovery,

        "status_labels": status_labels,

        "status_counts": status_counts,

        "value_labels": value_labels,

        "value_amounts": value_amounts,

    }

    return render(
        request,
        "analytics.html",
        context
    )