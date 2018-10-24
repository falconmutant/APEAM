from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from web.variables import *
# Create your models here.


class Menu(models.Model):
	name = models.TextField()
	icon = models.TextField()
	alive = models.BooleanField(default=True)

	def __str__(self):
		return "%s" % self.name


class CoreGadget(models.Model):
	name = models.TextField()
	category = models.CharField(choices=CATEGORY_GADGET, max_length=1)
	html = models.TextField()
	js = models.TextField()
	css = models.TextField(null=True, blank=True)
	alive = models.BooleanField(default=True)

	def __str__(self):
		return "%s" % self.name


class Gadget(models.Model):
	name = models.TextField()
	description = models.TextField()
	html = models.TextField(null=True, blank=True)
	js = models.TextField(null=True, blank=True)
	css = models.TextField(null=True, blank=True)
	config = JSONField(null=True, blank=True)
	alive = models.BooleanField(default=True)

	def __str__(self):
		return "%s" % self.name


class MenuGadget(models.Model):
	menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
	gadget = models.ManyToManyField(Gadget, blank=True)
	type = models.CharField(choices=TYPE_PROFILE, max_length=1, null=True)
	alive = models.BooleanField(default=True)

	def __str__(self):
		return "%s - %s" % (self.menu, self.gadget)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	type = models.CharField(choices=TYPE_PROFILE, max_length=1, null=True)
	config = JSONField(null=True)
	alive = models.BooleanField(default=True)

	def __str__(self):
		return "%s %s" % (self.user, self.get_type_display())
