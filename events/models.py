from django.db import models
from django.db.models import Min, Max, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
import uuid

from denorm import denormalized, depend_on_related


class PastEvent(models.Manager):
    def get_queryset(self):
        now = datetime.now()
        today = now.date()
        time = now.time()
        return super(PastEvent, self).get_queryset().filter(ends_date__lt=today, ends_time__lt=time)


class PublishedEvent(models.Manager):
    def get_queryset(self):
        now = datetime.now()
        today = now.date()
        time = now.time()
        return super(PublishedEvent, self).get_queryset().filter(published=True).filter(ends_date__gte=today,
                                                                                        ends_time__gte=time)


class PublishedPastEvent(models.Manager):
    def get_queryset(self):
        now = datetime.now()
        today = now.date()
        time = now.time()
        return super(PublishedEvent, self).get_queryset().filter(published=True).filter(ends_date__lt=today,
                                                                                        ends_time__lt=time)


class Event(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=150, default="", verbose_name="event name")
    subtitle = models.CharField(null=False, blank=False, max_length=150, default="", verbose_name="event subtitle")
    begins_date = models.DateField(null=True, verbose_name="starts")
    begins_time = models.TimeField(null=True, verbose_name="")
    ends_date = models.DateField(null=True, verbose_name="ends")
    ends_time = models.TimeField(null=True, verbose_name="")
    description = models.TextField(null=False, blank=False, verbose_name="description")
    cover = models.ImageField(null=True, verbose_name="cover image", upload_to='events/cover/')

    venue = models.CharField(null=False, blank=True, max_length=150, default="", verbose_name="venue name")
    address = models.CharField(null=False, blank=True, max_length=150, default="",
                               verbose_name="address (street name & number)")
    neighborhood = models.CharField(null=False, blank=True, max_length=150, default="")
    city = models.CharField(null=False, blank=True, max_length=150, default="")
    postal_code = models.CharField(null=False, blank=True, max_length=5, default="")

    organizer = models.ForeignKey(User, null=True)
    display_remaining_tickets = models.BooleanField(default=False)

    published = models.BooleanField(default=False)

    past = PastEvent()
    objects = models.Manager()
    publishedEvent = PublishedEvent()
    publishedPast = PublishedPastEvent()

    class Meta:
        ordering = ['begins_date', 'begins_time']

    @denormalized(models.DecimalField, max_digits=5, decimal_places=2, default=0)
    @depend_on_related('Ticket')
    def min_ticket_price(self):
        try:
            return self.tickets_types.all().aggregate(Min('price')).get('price__min') or 0
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.DecimalField, max_digits=5, decimal_places=2, default=0)
    @depend_on_related('Ticket')
    def max_ticket_price(self):
        try:
            return self.tickets_types.all().aggregate(Max('price')).get('price__max') or 0
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.IntegerField, default=0)
    @depend_on_related('Ticket')
    def total_tickets(self):
        try:
            return self.tickets_types.all().aggregate(Sum('total')).get('total__sum') or 0
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.IntegerField, default=0)
    @depend_on_related('TicketSales')
    def tickets_sold(self):
        try:
            return self.tickets_sales.all().count()
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.IntegerField, default=0)
    @depend_on_related('TicketSales')
    def tickets_available(self):
        return self.total_tickets - self.tickets_sold

    @property
    def admin_url(self):
        uuid = "{}".format(self.uuid)
        return reverse('my_events_update', kwargs={'event_uuid': uuid.replace("-", "")})

    @property
    def url(self):
        return self.admin_url

    @property
    def cover_url(self):
        try:
            return self.cover.url
        except:
            pass
        return 'https://placeholdit.imgix.net/~text?txtsize=33&txt=Event%20Image&w=256&h=256'

    def __str__(self):
        return "{} - {}({})".format(self.name, self.begins_date, self.begins_time)

    def define_ticket_type(self, pk, name, price, total):
        price = float(price or '1')
        total = int(total or '1')
        ticket = None
        if pk is not None and pk.strip():
            ticket = self.tickets_types.filter(pk=pk).first()
        if ticket is None:
            ticket = Ticket.objects.create(event=self, name=name, price=price or 1, total=total or 1)
        else:
            ticket.name = name
            ticket.price = price
            ticket.totla = total
            ticket.save()
        return ticket

    def clean_tickets(self, exclude=[]):
        kept_alive = []
        for ticket in self.tickets_types.all().exclude(pk__in=[e.pk for e in exclude]):
            if ticket.can_delete:
                ticket.delete()
            else:
                kept_alive.append(ticket)
        return kept_alive

    @property
    def tickets(self):
        return self.tickets_types.all()


class Ticket(models.Model):
    event = models.ForeignKey(Event, blank=False, null=False, related_name='tickets_types')
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.IntegerField(blank=False, null=False, default=1)

    @denormalized(models.IntegerField, default=0)
    @depend_on_related('TicketSales')
    def sold(self):
        try:
            return self.ticket_type_sales.filter(event=self.event).count()
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.IntegerField, default=0)
    @depend_on_related('TicketSales')
    def available(self):
        return self.total - self.sold

    @denormalized(models.CharField, null=False, blank=False, max_length=150, default='Selling')
    @depend_on_related('TicketSales')
    def status(self):
        if self.available == 0:
            return "Sold Out"
        return "Selling"

    @property
    def can_delete(self):
        if self.sold > 0:
            return False
        return True


class TicketSales(models.Model):
    event = models.ForeignKey(Event, blank=False, null=False, related_name='tickets_sales')
    ticket_type = models.ForeignKey(Ticket, blank=False, null=False, related_name='ticket_type_sales')
    buyer = models.ForeignKey(User, blank=False, null=False, related_name='tickets_bought')

    @denormalized(models.CharField, null=False, blank=False, max_length=150, default='NO NAME')
    def buyer_name(self):
        return ""


class PaymentCustomer(models.Model):
    uuid = models.UUIDField(editable=False, null=False, blank=False)
    user = models.ForeignKey(User, related_name='payment_customer')


class TicketSalesOrder(models.Model):
    buyer = models.ForeignKey(PaymentCustomer, related_name='tickets_sales_order', default=0)
    event = models.ForeignKey(Event, related_name='tickets_sells', default=0)
    ticket_type = models.ForeignKey(Ticket, related_name='tickets_type_sold', default=0)
    qty = models.IntegerField(default=1, null=False)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    transaction_uuid = models.CharField(max_length=100, null=False, blank=False, default=uuid.uuid4)


class ShoppingCart(models.Model):
    event = models.ForeignKey(Event, related_name='events_shopping_cart', default=0)
    buyer = models.ForeignKey(User, null=True, default=None)
    is_guest = models.BooleanField(default=False)
    active = models.BooleanField(default=True)


def generate_expiration_datetime(minutes=5):
    now = datetime.now()
    expiration_datetime = now + timedelta(minutes=minutes)
    return expiration_datetime


class TicketSelection(models.Model):
    cart = models.ForeignKey(ShoppingCart, default=0, null=False, related_name='tickets_selected')
    ticket_type = models.ForeignKey(Ticket, null=False, default=0)
    qty = models.IntegerField(default=1, null=False)
    expiration = models.DateTimeField(null=False, default=generate_expiration_datetime)

