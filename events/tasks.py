# Create your tasks here
from __future__ import absolute_import, unicode_literals
import celery
from utils.openpay_gateway import PaymentGateway
from django.contrib.auth.models import User
from django.core.mail import send_mail


@celery.task(name='events.tickets.reservation.check')
def check_tickets_reservation(ticket_id):
    from .models import TicketSelection
    try:
        ticket_selection = TicketSelection.objects.get(id=ticket_id)
        ticket_selection.check_ticket_reservation()
    except TicketSelection.DoesNotExist:
        pass


@celery.task# (name='events.tickets.checkout')
def process_ticket_purchase_order(cart_id, cc_number, cc_exp_month, cc_exp_year, cc_cvv, description):
    print("BEGIN TASK")
    from events.models import ShoppingCart
    # from utils.openpay_gateway import PaymentGateway
    cart = ShoppingCart.objects.get(id=cart_id)
    print("CART: {}".format(cart))
    from events.models import PaymentCustomer, PaymentCreditCard
    try:
        gateway = PaymentGateway()
        customer_id, to_create = gateway.set_customer(first_name=cart.first_name, last_name=cart.last_name,
                                                      email=cart.email, line1=cart.line1, line2=cart.line2,
                                                      line3=cart.line3, city=cart.city, state=cart.state,
                                                      postal_code=cart.postal_code, phone_number=cart.phone_number)
        print("gateway.set_customer: {}, {}".format(customer_id, to_create))
        card_id, cc_mask = gateway.set_credit_card(card_holder=cart.card_holder, number=cc_number, month=cc_exp_month,
                                                   year=cc_exp_year, cvv=cc_cvv)
        print("gateway.set_credit_card: {}, {}".format(card_id, cc_mask))
        total = float('{}'.format(cart.total))
        authorized, authorization, error_message = gateway.do_pay(amount=total, order_id=cart.order_id,
                                                                  description=description)
        print("gateway.do_pay: {}, {}".format(card_id, cc_mask))
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
            print("PaymentCustomer: {}, {}".format(payment_customer, created ))
            payment_cc, cc_created = PaymentCreditCard.objects.get_or_create(customer=payment_customer, uuid=card_id,
                                                                             credit_card_number=cc_mask)
            print("PaymentCreditCard: {}, {}".format(payment_cc, cc_created))

            # Assign tickets
            cart.asign_tickets(authorization=authorization, cc=payment_cc)
            # Send Email
#             send_ticket_purchase_notification_email.delay(email=cart.email, tikets=cart.tickets_selected,
#                                                          order_id=cart.order_id, cc_mask=cc_mask,
#                                                          autorization=authorization)
            task = send_ticket_purchase_notification_email.apply_async(kwargs={
                'email': cart.email,
                'tikets': cart.selected_tickets,
                'order_id': cart.order_id,
                'cc_mask': cc_mask,
                'autorization': authorization,
            })
        else:
            # Send Email with error
#            send_ticket_purchase_error_email.delay(email=cart.email, cc_mask=cc_mask, error=error_message)
            print('ERROR')
            task = send_ticket_purchase_error_email.apply_async(kwargs={
                'email': cart.email,
                'cc_mask': cc_mask,
                'error': error_message
            })
    except Exception as error:
        # Send Email with error
        print('EXCEPTION')
        error_message = '{}'.format(error)
        task = send_ticket_purchase_error_email.apply_async(kwargs={
            'email': cart.email,
            'cc_mask': None,
            'error': error_message
        })
    print("END TASK")


@celery.task# (name='events.tickets.checkout.notification')
def send_ticket_purchase_notification_email(email, tikets, order_id, cc_mask, autorization):
    subject = 'Your purchase order is ready'
    body = 'You purchase is ready'
    sender = 'purchase@fronesis.mx'
    recipient_list = [email, 'ricardo.tercero.solis@gmail.com']
    send_mail(subject, body, sender, recipient_list)


@celery.task# (name='events.tickets.checkout.error.notification')
def send_ticket_purchase_error_email(email, cc_mask, error):
    print('send_ticket_purchase_error_email - ERROR: {}'.format(error))
    subject = 'Your purchase order is ready'
    body = 'Error: {}'.format(error)
    sender = 'purchase@fronesis.mx'
    recipient_list = [email, 'ricardo.tercero.solis@gmail.com']
    send_mail(subject, body, sender, recipient_list)
