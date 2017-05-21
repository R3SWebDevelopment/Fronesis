# Create your tasks here
from __future__ import absolute_import, unicode_literals
import celery
from utils.openpay_gateway import PaymentGateway


@celery.task(name='events.tickets.reservation.check')
def check_tickets_reservation(ticket_id):
    from .models import TicketSelection
    try:
        ticket_selection = TicketSelection.objects.get(id=ticket_id)
        ticket_selection.check_ticket_reservation()
    except TicketSelection.DoesNotExist:
        pass


@celery.task
def process_ticket_purchase_order(card, cc_number, cc_exp_month, cc_exp_year, cc_cvv):
    pass
