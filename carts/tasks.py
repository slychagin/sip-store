from datetime import date
from celery import shared_task
from carts.models import Coupon

from django.core import management


@shared_task
def check_coupon():
    """
    Check every day all available coupons and set is_available coupon
    status to false if current date grater than validity date
    """
    coupons = Coupon.objects.filter(is_available=True)
    current_date = date.today()

    for coupon in coupons:
        if coupon.validity < current_date:
            coupon.is_available = False
            coupon.save()


# TODO: Настроить очистку сеансов с истекшим сроком действия (clearsessions)


@shared_task
def cleanup():
    """Cleanup expired sessions by using Django management command."""
    try:
        management.call_command("clearsessions", verbosity=0)
        return "success"
    except Exception as e:
        print(e)
