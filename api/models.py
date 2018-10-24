from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.fields import JSONField

from api.variable import *
# Create your models here.


class Farm(models.Model):
	hectares = models.FloatField()

	def __str__(self):
		return "%f" % self.hectares


class Contact(models.Model):
	type = models.CharField(choices=TYPE_CONTACT, max_length=1, null=True)
	contact = models.TextField()

	def __str__(self):
		return "%s %s" % (self.type, self.contact)


class Farmer(models.Model):
	last_name = models.TextField()
	last_name2 = models.TextField()
	name = models.TextField()
	gender = models.CharField(choices=GENDER, max_length=1, null=True)
	photo = models.ImageField(null=True)
	contact = models.ManyToManyField(Contact)
	address = JSONField(null=True)
	farm = models.ManyToManyField(Farm)
	search = SearchVectorField(null=True)
	alive = models.BooleanField(default=True)

	def __str__(self):
		return "%s %s" % (self.last_name, self.name)


class Logger(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	type = models.CharField(choices=LOGGER_STATUS, max_length=1, null=True)
	table = models.CharField(choices=TABLES, max_length=1, null=True)
	table_id = models.IntegerField()
	before = JSONField(null=True)
	after = JSONField(null=True)

	def __str__(self):
		return "%s %s" % (self.get_table_display(), self.table_id)


class TemplateMessage(models.Model):
	name = models.TextField()
	text = models.TextField()

	def __str__(self):
		return "%s" % self.name


class OutboundMessage(models.Model):
	name = models.TextField()
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	template = models.ForeignKey(TemplateMessage, on_delete=models.CASCADE)
	date = models.DateTimeField()

	def __str__(self):
		return "%s %s" % (self.name, self.date)


class OutboundFarmer(models.Model):
	out = models.ForeignKey(OutboundMessage, on_delete=models.CASCADE)
	farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)

	def __str__(self):
		return "%s %s" % (self.out, self.farmer)


class InboundMessage(models.Model):
	sender = models.ForeignKey(Farmer, on_delete=models.CASCADE)
	date = models.DateTimeField()
	message = models.TextField()

	def __str__(self):
		return "%s %s" % (self.sender, self.date)

