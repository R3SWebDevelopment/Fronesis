# Create your tasks here
from __future__ import absolute_import, unicode_literals
import celery
from utils.openpay_gateway import PaymentGateway
from django.contrib.auth.models import User
from utils.utils import send_email
from .models import ServicePayment
from datetime import datetime


@celery.task
def check_tickets_reservation(ticket_id):
    from .models import TicketSelection
    try:
        ticket_selection = TicketSelection.objects.get(id=ticket_id)
        ticket_selection.check_ticket_reservation()
    except TicketSelection.DoesNotExist:
        pass


@celery.task
def process_service_payment(payment_info):
    print("payment_info: {}".format(payment_info))
    first_name = payment_info.get('first_name')
    last_name = payment_info.get('last_name')
    email = payment_info.get('email')
    line1 = payment_info.get('line1')
    line2 = payment_info.get('line2')
    line3 = payment_info.get('line3')
    city = payment_info.get('city')
    state = payment_info.get('state')
    postal_code = payment_info.get('postal_code')
    phone_number = payment_info.get('phone_number')
    card_holder = payment_info.get('card_holder')
    cc_number = payment_info.get('credit_card_number')
    cc_exp_month = payment_info.get('credit_card_exp_month')
    cc_exp_year = payment_info.get('credit_card_exp_year')
    cc_cvv = payment_info.get('credit_card_cvv')
    order_id = payment_info.get('order')
    description = payment_info.get('description')
    total = payment_info.get('amount')
    try:
        gateway = PaymentGateway()
        customer_id, to_create = gateway.set_customer(first_name=first_name, last_name=last_name,
                                                      email=email, line1=line1, line2=line2,
                                                      line3=line3, city=city, state=state,
                                                      postal_code=postal_code, phone_number=phone_number)

        card_id, cc_mask = gateway.set_credit_card(card_holder=card_holder, number=cc_number, month=cc_exp_month,
                                                   year=cc_exp_year, cvv=cc_cvv)

        total = float('{}'.format(total))
        authorized, authorization, error_message = gateway.do_pay(amount=total, order_id=order_id,
                                                                  description=description)

        if authorized:
            # SEND EMAIL AND CHANGE FLAG
            service_payment = ServicePayment.objects.filter(pk=order_id).first()
            if service_payment:
                service_payment.auth_number = authorization
                service_payment.credit_card = cc_mask
                service_payment.processed_timestamp = datetime.now()
                service_payment.save()
                service = service_payment.service
                if service:
                    service.already_paid = True
                    service.save()
            print("PAYMENT COLLECTED FROM {} WITH AUTH NUMBER {}".format(cc_mask, authorization))

        else:
            # Send Email with error
            print("THERE WAS AN ERROR")
    except Exception as error:
        # Send Email with error
        error_message = '{}'.format(error)
        print("THERE WAS AN ERROR: {}".format(error_message))


@celery.task
def process_ticket_purchase_order(cart_id, cc_number, cc_exp_month, cc_exp_year, cc_cvv, description):
    from events.models import ShoppingCart
    cart = ShoppingCart.objects.get(id=cart_id)

    from events.models import PaymentCustomer, PaymentCreditCard
    try:
        gateway = PaymentGateway()
        customer_id, to_create = gateway.set_customer(first_name=cart.first_name, last_name=cart.last_name,
                                                      email=cart.email, line1=cart.line1, line2=cart.line2,
                                                      line3=cart.line3, city=cart.city, state=cart.state,
                                                      postal_code=cart.postal_code, phone_number=cart.phone_number)

        card_id, cc_mask = gateway.set_credit_card(card_holder=cart.card_holder, number=cc_number, month=cc_exp_month,
                                                   year=cc_exp_year, cvv=cc_cvv)

        total = float('{}'.format(cart.total))
        authorized, authorization, error_message = gateway.do_pay(amount=total, order_id=cart.order_id,
                                                                  description=description)

        if authorized:
            # If need it create user
            if to_create:
                user = User.objects.create(email=cart.email, username=cart.email, first_name=cart.first_name,
                                           last_name=cart.last_name)
                user.save()
            else:
                user = User.objects.get(email=cart.email)
            cart.assign_user(user)

            payment_customer, created = PaymentCustomer.objects.get_or_create(uuid=customer_id, user=user)

            payment_cc, cc_created = PaymentCreditCard.objects.get_or_create(customer=payment_customer, uuid=card_id,
                                                                             credit_card_number=cc_mask)

            # Assign tickets
            purchared_tickets = cart.asign_tickets(authorization=authorization, cc=payment_cc)
            # Send Email
            purchared_tickets_dict = [{
                'price': ticket.price,
                'name': ticket.name,
                'uuid': ticket.uuid,
            } for ticket in purchared_tickets]
            task = send_ticket_purchase_notification_email.apply_async(kwargs={
                'email': cart.email,
                'tickets': purchared_tickets_dict,
                'order_id': cart.order_id,
                'cc_mask': cc_mask,
                'authorization': authorization,
                'buyer': user.get_full_name(),
                'total': total,
            })
        else:
            # Send Email with error
            task = send_ticket_purchase_error_email.apply_async(kwargs={
                'email': cart.email,
                'cc_mask': cc_mask,
                'error': error_message,
                'total': total,
                'order_id': cart.order_id,
                'buyer': '{} {}'.format(cart.first_name, cart.last_name),
            })
    except Exception as error:
        # Send Email with error
        error_message = '{}'.format(error)
        task = send_ticket_purchase_error_email.apply_async(kwargs={
            'email': cart.email,
            'cc_mask': None,
            'error': error_message,
            'order_id': cart.order_id,
            'buyer': '{} {}'.format(cart.first_name, cart.last_name),
            'total': cart.total,
        })


@celery.task
def send_ticket_purchase_notification_email(email, tickets, order_id, cc_mask, authorization, buyer, total):
    template_file = 'events/ticket-purchase-notification.html'

    context_data = {
        'tickets': tickets,
        'order': order_id,
        'credit_card': cc_mask,
        'authorization': authorization,
        'name': buyer,
        'total': total,
    }
    subject = 'Fronesis - Tickets Purchase Notification'
    recepiants = [email]
    send_email(template_file=template_file, context_data=context_data, subject=subject, recepiants=recepiants)


@celery.task
def send_ticket_purchase_error_email(email, cc_mask, error, order_id, buyer, total='0.00'):
    template_file = 'events/ticket-purchase-error-notification.html'
    context_data = {
        'order': order_id,
        'credit_card': cc_mask,
        'name': buyer,
        'total': total,
        'error': error,
    }
    subject = 'Fronesis - Tickets Purchase Notification'
    recepiants = [email]
    send_email(template_file=template_file, context_data=context_data, subject=subject, recepiants=recepiants)

