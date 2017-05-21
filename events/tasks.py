# Create your tasks here
from __future__ import absolute_import, unicode_literals
import celery
from utils.openpay_gateway import PaymentGateway
from django.contrib.auth.models import User


@celery.task(name='events.tickets.reservation.check')
def check_tickets_reservation(ticket_id):
    from .models import TicketSelection
    try:
        ticket_selection = TicketSelection.objects.get(id=ticket_id)
        ticket_selection.check_ticket_reservation()
    except TicketSelection.DoesNotExist:
        pass


@celery.task
def process_ticket_purchase_order(card, cc_number, cc_exp_month, cc_exp_year, cc_cvv, description):
    # from utils.openpay_gateway import PaymentGateway
    try:
        gateway = PaymentGateway()
        customer_id, to_create = gateway.set_customer(first_name=card.first_name, last_name=card.last_name,
                                                      email=card.email, line1=card.line1, line2=card.line2,
                                                      line3=card.line3, city=card.city, state=card.state,
                                                      postal_code=card.postal_code, phone_number=card.phone_number)

        card_id, cc_mask = gateway.set_credit_card(card_holder=card.card_holder, number=cc_number, month=cc_exp_month,
                                                   year=cc_exp_year, cvv=cc_cvv)

        authorized, authorization, error_message = gateway.do_pay(amount=card.total, order_id=card.order_id,
                                                                  description=description)
        if authorized:
            # If need it create user
            if to_create:
                user = User.objects.create(email=card.email, username=card.email, first_name=card.first_name,
                                           last_name=card.last_name)
                user.save()
                card.assign_user(user)
            # Assign tickets
            card.asign_tickets(cc_mask=cc_mask, authorization=authorization)
            # Send Email
            send_ticket_purchase_notification_email.delay(email=card.email, tikets=card.tickets_selected,
                                                          order_id=card.order_id, cc_mask=cc_mask,
                                                          autorization=authorization)
        else:
            # Send Email with error
            send_ticket_purchase_error_email.delay(email=card.email, cc_mask=cc_mask, error=error_message)
    except Exception as error:
        # Send Email with error
        pass


@celery.task
def send_ticket_purchase_notification_email(email, tikets, order_id, cc_mask, autorization):
    pass

@celery.task
def send_ticket_purchase_error_email(email, cc_mask, error):
    pass
