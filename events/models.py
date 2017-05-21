from django.template.defaultfilters import slugify
from django.db import models
from django.db.models import Min, Max, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
from django.db.models import Q
import uuid
from django.contrib.humanize.templatetags.humanize import intcomma
from .tasks import check_tickets_reservation


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
        qs_events_later_today = Q(begins_date=today, begins_time__gte=time)
        qs_events_after_today = Q(begins_date__gt=today)
        return super(PublishedEvent, self).get_queryset().filter(published=True).\
            filter(qs_events_later_today | qs_events_after_today)


class PublishedPastEvent(models.Manager):
    def get_queryset(self):
        now = datetime.now()
        today = now.date()
        time = now.time()
        qs_events_before_today = Q(ends_date__lt=today)
        qs_events_early_today = Q(ends_date=today, ends_time__lt=time)
        return super(PublishedPastEvent, self).get_queryset().filter(published=True).\
            filter(qs_events_before_today | qs_events_early_today)


class PublishedAllEvent(models.Manager):
    def get_queryset(self):
        return super(PublishedAllEvent, self).get_queryset().filter(published=True)


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

    slug = models.SlugField(max_length=250, null=True, blank=True, default="")

    past = PastEvent()
    objects = models.Manager()
    publishedEvent = PublishedEvent()
    publishedPast = PublishedPastEvent()
    published_all = PublishedAllEvent()

    class Meta:
        ordering = ['begins_date', 'begins_time']

    @property
    def assistants(self):
        return User.objects.all()

    @property
    def organizer_name(self):
        return self.organizer.get_full_name()

    @property
    def begins_timestamp(self):
        return datetime.combine(self.begins_date, self.begins_time)

    @property
    def ends_timestamp(self):
        return datetime.combine(self.ends_date, self.ends_time)

    @denormalized(models.DecimalField, max_digits=8, decimal_places=2, default=0)
    @depend_on_related('Ticket')
    def min_ticket_price(self):
        try:
            return self.tickets_types.all().aggregate(Min('price')).get('price__min') or 0
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.DecimalField, max_digits=8, decimal_places=2, default=0)
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
    def sells_percentage(self):
        return (self.tickets_sold * 100) / self.total_tickets

    @property
    def admin_url(self):
        uuid = "{}".format(self.uuid)
        return reverse('my_events_update', kwargs={'event_uuid': uuid})

    @property
    def url(self):
        year = self.begins_date.year
        month = self.begins_date.strftime('%B')
        day = self.begins_date.day
        return reverse('public_event', kwargs={
            'year': year,
            'month': month,
            'day': day,
            'slug': self.slug,
            'event_uuid': self.uuid
        })

    @property
    def get_tickets_url(self):
        year = self.begins_date.year
        month = self.begins_date.strftime('%B')
        day = self.begins_date.day
        return reverse('public_event_tickets', kwargs={
            'year': year,
            'month': month,
            'day': day,
            'slug': self.slug,
            'event_uuid': self.uuid
        })

    @property
    def get_tickets_checkout_url(self):
        year = self.begins_date.year
        month = self.begins_date.strftime('%B')
        day = self.begins_date.day
        return reverse('public_event_tickets_checkout', kwargs={
            'year': year,
            'month': month,
            'day': day,
            'slug': self.slug,
            'event_uuid': self.uuid
        })

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
        if name is not None and name.strip():
            price = "%.2f" % round(float(price), 2)
            total = int(total or '1')
            ticket = None
            if pk is not None and pk.strip():
                ticket = self.tickets_types.filter(pk=pk).first()
            if ticket is None:
                ticket = Ticket.objects.create(event=self, name=name, price=price, total=total)
            else:
                ticket.name = name
                ticket.price = price
                ticket.total = total
                ticket.save()
            return ticket
        else:
            return None

    def clean_tickets(self, exclude=[]):
        kept_alive = []
        for ticket in self.tickets_types.all().exclude(pk__in=[e.pk for e in exclude if e is not None]):
            if ticket.can_delete:
                ticket.delete()
            else:
                kept_alive.append(ticket)
        return kept_alive

    @property
    def tickets(self):
        return self.tickets_types.all()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)


class Ticket(models.Model):
    event = models.ForeignKey(Event, blank=False, null=False, related_name='tickets_types')
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.IntegerField(blank=False, null=False, default=1)

    class Meta:
        ordering = ['price', 'name']

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
    credit_card = models.ForeignKey('PaymentCreditCard', blank=False, null=False, default=0,
                                    related_name='tickets_bought')
    payment_authorization = models.CharField(null=False, blank=False, default='99999999', max_length=30)
    uuid = models.UUIDField(editable=False, null=False, blank=False, default=uuid.uuid4)

    @denormalized(models.CharField, null=False, blank=False, max_length=150, default='NO NAME')
    def buyer_name(self):
        return ""


class PaymentCustomer(models.Model):
    uuid = models.UUIDField(editable=False, null=False, blank=False)
    user = models.ForeignKey(User, related_name='payment_customer')


class PaymentCreditCard(models.Model):
    customer = models.ForeignKey(PaymentCustomer, blank=False, null=False, default=0, related_name='credit_card')
    uuid = models.UUIDField(editable=False, null=False, blank=False)
    credit_card_number = models.CharField(max_length=19, null=False, blank=False, default='**** **** **** ****')


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
    selected = models.BooleanField(default=False)
    checkout = models.BooleanField(default=False)

    first_name = models.CharField(blank=True, null=True, default='', max_length=100)
    last_name = models.CharField(blank=True, null=True, default='', max_length=100)
    line1 = models.CharField(blank=True, null=True, default='', max_length=150, verbose_name='Street Name')
    line2 = models.CharField(blank=True, null=True, default='', max_length=150, verbose_name='Neighborhood')
    line3 = models.CharField(blank=True, null=True, default='', max_length=150, verbose_name='City and State')
    email = models.CharField(blank=True, null=True, default='', max_length=150)
    phone_number = models.CharField(blank=True, null=True, default='', max_length=10)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.is_guest = self.buyer is None
            if self.is_guest is False:
                self.first_name = self.buyer.first_name
                self.last_name = self.buyer.last_name
                self.email = self.buyer.email
        super(ShoppingCart, self).save(*args, **kwargs)

    def update_event_tickets(self):
        for ticket in self.event.tickets:
            ticket_selection, created = TicketSelection.objects.get_or_create(cart=self, ticket_type=ticket)
            if created:
                ticket_selection.qty = 0
                ticket_selection.selected = False
                ticket_selection.expiration = None
                ticket_selection.save()

    @property
    def total(self):
        total = 0
        for ticket in self.tickets_selected.filter(selected=True):
            total += ticket.total
        return total

    @property
    def total_label(self):
        return intcomma(self.total)

    def asign_tickets(self):
        pass

    @property
    def tickets_selected(self):
        return self.tickets_selected.filter(selected=True).filter(qty__gt=0)


def generate_expiration_datetime(minutes=5):
    now = datetime.now()
    expiration_datetime = now + timedelta(minutes=minutes)
    return expiration_datetime


class TicketSelection(models.Model):
    cart = models.ForeignKey(ShoppingCart, default=0, null=False, related_name='tickets_selected')
    ticket_type = models.ForeignKey(Ticket, null=False, default=0)
    qty = models.IntegerField(default=0, null=False)
    expiration = models.DateTimeField(null=True, default=None)
    selected = models.BooleanField(default=False)

    class Meta:
        order_with_respect_to = 'ticket_type'

    @property
    def total(self):
        if self.selected:
            return self.qty * self.ticket_type.price
        return 0

    def select_ticket(self):
        self.selected = True
        self.expiration = generate_expiration_datetime()
        self.save()
        # Execute a ticket reservation check one second later the expiration date
        check_tickets_reservation.apply_async(eta=self.expiration + timedelta(seconds=1))

    def check_ticket_reservation(self):
        # Checks if the ticket reservation time has expired, if does release the tickets and clear the expiration
        now = datetime.now()
        if self.selected and now > self.expiration:
            self.selected = False
            self.qty = 0
            self.expiration = None
            self.save()
