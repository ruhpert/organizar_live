# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

SEX = (
	('m', 'Herr'),
	('f', 'Frau'),
)


class Subject(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name = "Fach"
		verbose_name_plural = "Fächer"

class Grade(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Klasse"
		verbose_name_plural = "Klassen"

class School(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name = "Schule"
		verbose_name_plural = "Schulen"


# TODO find better naming 
class Child_Contact(models.Model):
	grade = models.OneToOneField(Grade, blank=True, null=True) # new
	school = models.OneToOneField(School, blank=True, null=True) # new

	def __unicode__(self):
		return self.child.street

	class Meta:
		verbose_name = "Schüler"
		verbose_name_plural = "Schüler"

class Billing_Type(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Rechnungstyp"
		verbose_name_plural = "Rechnungstypen"

class Billing_Contact(models.Model):
	knr = models.CharField(max_length=200, blank=True, null=True)
	blz = models.CharField(max_length=200, blank=True, null=True)
	iban = models.CharField(max_length=200, blank=True, null=True)
	iban = models.CharField(max_length=200, blank=True, null=True)
	billing_type = models.OneToOneField(Billing_Type, blank=True, null=True)

	def __unicode__(self):
		return self.person.user.last_name

	class Meta:
		verbose_name = "Rechnungsadresse"
		verbose_name_plural = "Rechnungsadressen"

class Person(models.Model):
	sex = models.CharField("Geschlecht", max_length=1, choices=SEX, blank=True, null=True)
	birthday = models.DateField("Geburtstag", blank=True, null=True) # new
	street = models.CharField("Strasse", max_length=200, blank=True, null=True)
	hnr = models.CharField("Hausnummer", max_length=10, blank=True, null=True)
	zip = models.IntegerField("PLZ", max_length=8, blank=True, null=True)
	city = models.CharField("Stadt", max_length=200, blank=True, null=True)
	country = models.CharField("Land", max_length=200, blank=True, null=True) # new
	phone = models.CharField("Telefon", max_length=200, blank=True, null=True)
	mobile = models.CharField("Handy", max_length=200, blank=True, null=True)
	accessibility = models.CharField("Mögliche Termine oder Zeiten wo unmöglich gehen.", max_length=600, blank=True, null=True) # new
	user = models.OneToOneField(User)
	child_contact = models.OneToOneField(Child_Contact)
	billing_contact = models.OneToOneField(Billing_Contact)

	def __unicode__(self):
		return str(self.mobile)
	
	def get_user(self):
		return self.user

	class Meta:
		verbose_name = "Benutzer"
		verbose_name_plural = "Benutzer"

