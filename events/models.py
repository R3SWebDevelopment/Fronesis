from django.db import models
from django.db.models import Min, Max, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.urls import reverse
import uuid

from denorm import denormalized, depend_on_related


class Event(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=150, default="", verbose_name="event name")
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


class TicketSalesOrder(models.Model):
    pass
