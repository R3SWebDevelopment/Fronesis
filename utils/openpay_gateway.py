from django.contrib.auth.models import User
import openpay
import os

####TESTING
# from utils.openpay_gateway import PaymentGateway
# gateway = PaymentGateway()
# gateway.set_customer(first_name='Leonardo', last_name='Tercero Solis', email='tercero3@hotmail.com', line1='Narciso Serradel 16', line2='Col. Indeco Animas', line3='aa', city='Xalapa', state='Veracruz', postal_code='91190', phone_number='2288128877')
# gateway.set_credit_card(card_holder='Blanca Lilia Solis Campos', number='4111111111111111', month='12', year='2020', cvv='110')
# gateway.do_pay(amount=100.00, order_id='11212213', description='Test')

class PaymentGateway(object):
    payment_customer = None
    customer = None
    payment_credit_card = None
    card = None
    charge = None
    card_error = None
    customer_error = None
    address = {}
    card_dict = {}
    payment_error = None
    debut = True

    def __init__(self):
        openpay.api_key = '{}'.format(os.environ.get('OPENPAY_API_KEY'))
        openpay.verify_ssl_certs = os.environ.get('OPENPAY_VERIFY_SSL_CERTS') == 'True'
        openpay.merchant_id = '{}'.format(os.environ.get('OPENPAY_MERCHANT_ID'))
        openpay.production = os.environ.get('OPENPAY_PRODUCTION') == 'True'
        self.debut = not openpay.production

    def set_customer(self, first_name, last_name, email, line1, line2, line3, city, state, postal_code, phone_number,
                     country_code='MX'):
        to_create = True
        from events.models import PaymentCustomer
        user = User.objects.filter(email=email).first()
        self.address = {
            "city": city,
            "state": state,
            "line1": line1,
            "line2": line2,
            "line3": line3,
            "postal_code": postal_code,
            "country_code": country_code
        }
        if user is not None:
            to_create = False
            try:
                self.payment_customer = PaymentCustomer.objects.get(user=user)
                self.customer = openpay.Customer.retrieve(self.payment_customer.uuid)
                self.customer.name = first_name
                self.customer.last_name = last_name
                self.customer.phone_number = phone_number
                self.customer.address = self.address
                self.customer.save()
            except (PaymentCustomer.DoesNotExist, openpay.error.InvalidRequestError) as customer_error:
                self.customer_error = customer_error
                try:
                    self.customer = openpay.Customer.create(
                        name=first_name,
                        last_name=last_name,
                        email=email,
                        phone_number=phone_number,
                        address=self.address
                    )
                    self.customer_error = None
                except openpay.error.InvalidRequestError as customer_error:
                    self.customer_error = customer_error
        else:
            try:
                self.customer = openpay.Customer.create(
                    name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    address=self.address
                )
                self.customer_error = None
            except openpay.error.InvalidRequestError as customer_error:
                self.customer_error = customer_error
                return None, False
        return self.customer.id, to_create

    def set_credit_card(self, card_holder, number, month, year, cvv):
        if self.debut:
            number = '4111111111111111'
            month = '12'
            year = '2020'
            cvv = '110'
        from events.models import PaymentCreditCard
        credit_card_mask = '**** **** **** {}'.format(number[-4:])
        try:
            self.payment_credit_card = PaymentCreditCard.objects.get(customer=self.payment_customer,
                                                                     credit_card_number=credit_card_mask)
            self.card = self.customer.cards.retrieve(self.payment_credit_card.uuid)
            self.card.holder_name = card_holder
            self.card.save()
        except (PaymentCreditCard.DoesNotExist, NameError, openpay.error.InvalidRequestError):
            try:
                self.card_dict = {
                    'card_number': number,
                    'holder_name': card_holder,
                    'expiration_year': year[-2:],
                    'expiration_month': month,
                    'cvv2': cvv,
                    'address': self.address
                }
                self.card = self.customer.cards.create(
                    card_number=number,
                    holder_name=card_holder,
                    expiration_year=year[-2:],
                    expiration_month=month,
                    cvv2=cvv,
                    address=self.address
                )
            except openpay.error.CardError as card_error:
                self.card_error = '{}'.format(card_error)
        return self.card.get('id'), credit_card_mask

    def do_pay(self, amount, order_id, description, device_session_id="kjsadkjnnkjfvknjdfkjnvdkjnfvkj",):
        authorized = False
        authorization = None
        error_message = None
        try:
            self.charge = self.customer.charges.create(
                method="card",
                amount=amount,
                description=description,
                order_id=order_id,
                source_id=self.card.id,
                device_session_id=device_session_id
            )
            authorized = True
            print("do_pay - authorized: {}".format(authorized))
            print("do_pay - dir(self.charge): {}".format(dir(self.charge)))
            authorization = self.charge.authorization
            print("do_pay - authorization: {}".format(self.charge.authorization))
        except openpay.error.InvalidRequestError as payment_error:
            self.payment_error = payment_error
            error_message = '{}'.format(payment_error)
        return authorized, authorization, error_message
