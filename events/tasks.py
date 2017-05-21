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
def process_ticket_purchase_order(cart, cc_number, cc_exp_month, cc_exp_year, cc_cvv, description):
    # from utils.openpay_gateway import PaymentGateway
    from events.models import PaymentCustomer, PaymentCreditCard
    try:
        gateway = PaymentGateway()
        customer_id, to_create = gateway.set_customer(first_name=cart.first_name, last_name=cart.last_name,
                                                      email=cart.email, line1=cart.line1, line2=cart.line2,
                                                      line3=cart.line3, city=cart.city, state=cart.state,
                                                      postal_code=cart.postal_code, phone_number=cart.phone_number)

        card_id, cc_mask = gateway.set_credit_card(card_holder=cart.card_holder, number=cc_number, month=cc_exp_month,
                                                   year=cc_exp_year, cvv=cc_cvv)

        authorized, authorization, error_message = gateway.do_pay(amount=cart.total, order_id=cart.order_id,
                                                                  description=description)
        if authorized:
            # If need it create user
            if to_create:
                user = User.objects.create(email=cart.email, username=cart.email, first_name=cart.first_name,
                                           last_name=cart.last_name)
                user.save()

                cart.assign_user(user)
            else:
                user = User.objects.get(email=cart.email)

            payment_customer, created = PaymentCustomer.objects.get_or_create(uuid=customer_id, user=user)
            payment_cc, cc_created = PaymentCreditCard.objects.get_or_create(customer=payment_customer, uuid=card_id,
                                                                             credit_card_number=cc_mask)

            # Assign tickets
            cart.asign_tickets(authorization=authorization, cc=payment_cc)
            # Send Email
            send_ticket_purchase_notification_email.delay(email=cart.email, tikets=cart.tickets_selected,
                                                          order_id=cart.order_id, cc_mask=cc_mask,
                                                          autorization=authorization)
        else:
            # Send Email with error
            send_ticket_purchase_error_email.delay(email=cart.email, cc_mask=cc_mask, error=error_message)
    except Exception as error:
        # Send Email with error
        pass


@celery.task
def send_ticket_purchase_notification_email(email, tikets, order_id, cc_mask, autorization):
    pass

@celery.task
def send_ticket_purchase_error_email(email, cc_mask, error):
    pass
