from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django.utils.timezone import timedelta

from .models import Loan
from .services import notification

from usuarios.services import UserService

logger = get_task_logger(__name__)


@shared_task
def notify_due_date():
    target = timezone.now().date() + timedelta(days=1)
    loans = Loan.objects.filter(status=Loan.ACTIVE, due_date=target)

    for loan in loans:
        try:
            notification.due_date_tomorrow_info(loan)
        except Exception as e:
            logger.exception(
                f"Erro ao notificar loan {loan.id}: {e}"
            )

@shared_task
def update_loan_status_overdue():
    today = timezone.now().date()
    loans = Loan.objects.filter(
        status=Loan.ACTIVE, 
        due_date__lt=today
    ).select_related('borrower')

    for loan in loans:
        try:
            UserService.decrease_user_score(loan.borrower.id)
            loan.status = Loan.OVERDUE
            loan.save(update_fields=['status'])
            notification.overdue_loan_info(loan)
        except Exception as e:
            logger.exception(
                f"Erro ao processar loan {loan.id}: {e}"
            )