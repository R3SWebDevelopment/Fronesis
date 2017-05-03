from django.db import models
from django.db.models import Min, Max, Sum
from django.core.exceptions import ObjectDoesNotExist
import uuid

from denorm import denormalized, depend_on_related


class Event(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4(), editable=False, null=False, blank=False)
    title = models.CharField(null=False, blank=False, max_length=150)
    subtitle = models.CharField(null=True, blank=True, max_length=150)
    description = models.TextField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    duration = models.Duration(null=False)
    location = models.CharField(null=False, default=False, max_length=150)
    venue = models.CharField(null=False, default=False, max_length=150)
    address = models.TextField(null=True, default=True)
    cover = models.ImageField(null=True)
    organizer = models.ManyToManyField('users.UserProfile')
    tickets_selling_begins_date = models.DateField(null=False)
    tickets_selling_ends_date = models.DateField(null=False)

    @denormalized(models.DecimalField, max_digits=5, decimal_places=2)
    @depend_on_related('Ticket')
    def min_ticket_price(self):
        try:
            return self.tickets_types.all().aggregate(Min('price')).get('price__min') or 0
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.DecimalField, max_digits=5, decimal_places=2)
    @depend_on_related('Ticket')
    def max_ticket_price(self):
        try:
            return self.tickets_types.all().aggregate(Max('price')).get('price__max') or 0
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.IntegerField)
    @depend_on_related('Ticket')
    def total_tickets(self):
        try:
            return self.tickets_types.all().aggregate(Sum('total')).get('total__sum') or 0
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.IntegerField)
    @depend_on_related('TicketSales')
    def tickets_sold(self):
        try:
            return self.tickets_sales.all().count()
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.IntegerField)
    @depend_on_related('TicketSales')
    def tickets_available(self):
        return self.total_tickets - self.tickets_sold


class Ticket(models.Model):
    event = models.ForeignKey('Event', blank=False, null=False, related_name='tickets_types')
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.IntegerField(blank=False, null=False, default=1)

    @denormalized(models.IntegerField)
    @depend_on_related('TicketSales')
    def sold(self):
        try:
            return self.ticket_type_sales.filter(event=self.event).count()
        except ObjectDoesNotExist:
            return 0

    @denormalized(models.IntegerField)
    @depend_on_related('TicketSales')
    def available(self):
        return self.total - self.sold

    @denormalized(models.CharField, null=False, blank=False, max_length=150)
    @depend_on_related('TicketSales')
    def status(self):
        if self.available == 0:
            return "Sold Out"
        return "Selling"


class TicketSales(models.Model):
    event = models.ForeignKey('Event', blank=False, null=False, related_name='tickets_sales')
    ticket_type = models.ForeignKey('Ticket', blank=False, null=False, related_name='ticket_type_sales')
    buyer = models.ForeignKey('users.UserProfile', blank=False, null=False, related_name='tickets_bought')

    @denormalized(models.CharField, null=False, blank=False, max_length=150)
    def buyer_name(self):
        return ""


class TicketSalesOrder(models.Model):
    pass
