# coding=UTF-8

from django.db import models
import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from calendar import monthrange
import traceback
import sys 
from apps._person.models import Person

DUN_LEVEL = (
	('1', 'First'),
	('2', 'Second'),
	('3', 'Third'),
)

ACCOUNT_TYPE = (
	('activa', 'Activa'),
	('passiva', 'Passiva'),
)

class Amount(models.Model):
	amount = models.IntegerField(max_length=1)

	def __unicode__(self):
		return str(self.amount)

	class Meta:
		verbose_name = "Teilnamehäufigkeit"
		verbose_name_plural = "Teilnamehäufigkeiten"

class Duration(models.Model):
	duration = models.DecimalField("Dauer / Minuten", max_digits=5, decimal_places=2, blank=True, null=True)

	def __unicode__(self):
		return str(self.duration)

	class Meta:
		verbose_name = "Dauer"
		verbose_name_plural = "Dauer"


class Product(models.Model):
	name = models.CharField(max_length=200)
	charge = models.DecimalField("Kosten / Stunde", max_digits=5, decimal_places=2, blank=True, null=True)
	duration = models.OneToOneField(Duration, default=1)
	amount = models.OneToOneField(Amount, default=1)
	months = models.IntegerField(max_length=2, blank=True, null=True)
	days_a_week = models.IntegerField(max_length=1, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.charge)

	class Meta:
		verbose_name = "Produkt"
		verbose_name_plural = "Produkte"


class Discount(models.Model):
	discount = models.CharField("Rabatt", max_length=200)
	name = models.CharField("Name", max_length=200)

	def __unicode__(self):
		return str(self.name) + " " + str(self.discount) + "%"

	class Meta:
		verbose_name = "Rabatt"
		verbose_name_plural = "Rabatte"


class Contract(models.Model):
	number = models.CharField("Vertragsnummer", max_length=200)
	products =models.ManyToManyField(Product, blank=True, null=True, related_name='products')
	start_date = models.DateField("Start Date", default=datetime.date.today)
	end_date = models.DateField("End Date", default=datetime.date.today)
	#charge = models.ForeignKey(Charge)
	contact = models.OneToOneField(User,related_name='contract_contact')
	billing_contact = models.OneToOneField(User,related_name='contract_billing_contact')
	#duration = models.ForeignKey(Duration)
	#frequency = models.ForeignKey(Frequency)
	discount = models.ManyToManyField(Discount, blank=True, null=True, related_name='contract_discounts')

	def __unicode__(self):
		return self.number

	def get_frequency_per_week(self):
		return self.type.frequency.frequency / 4

	def calc_price(self):
		x = None

		try:
			x = float(self.type.frequency.frequency) * float(self.type.charge.charge)
		except:
			traceback.print_exc(file=sys.stdout)

		return float(x)

	def get_discounts(self):
		discounts = []
		try:
			x = self.calc_price()

			if x != None:
				for discount in self.discount.all():	
					discount_data = {}
					d = x * (float(discount.discount)/100)
					discount_data["amount"] = float(d)
					discount_data["name"] = discount.name
					discount_data["discount"] = discount.discount
					discounts.append(discount_data)
		except:
			traceback.print_exc(file=sys.stdout)	

		return discounts


	def calc_summ(self):
		summ = None
		registration_fee = 39

		try:
			summ = self.calc_price() + registration_fee
			discounts = self.get_discounts()

			for discount in discounts:
				summ = summ - discount["amount"]
		except:
			traceback.print_exc(file=sys.stdout)	

		return summ
	
	def calc_summ_without_fee(self):
		registration_fee = 39
		summ = self.calc_summ()
		summ = summ - registration_fee

		return summ

	def calc_month_difference(self):
		d1 = self.start_date
		d2 = self.end_date 
		delta = 0

		while True:
			mdays = monthrange(d1.year, d1.month)[1]
			d1 += timedelta(days=mdays)
			if d1 <= d2:
				delta += 1
			else:
				break

		return delta

	class Meta:
		verbose_name = "Vertrag"
		verbose_name_plural = "Verträge"

# Mahnung
class Dun(models.Model):
	level = models.CharField("Mahnlevel", max_length=1, choices=DUN_LEVEL, default=1)


class Invoice(models.Model):
	number = models.CharField("Rechnungsnummer", max_length=200)
	contract = models.OneToOneField(Contract)
	date = models.DateField()
	payed = models.BooleanField()
	dun = models.OneToOneField(Dun)

	def __unicode__(self):
		return (str(self.number) + " " + str(self.person.name))
	
	class Meta:
		verbose_name = "Rechnung"
		verbose_name_plural = "Rechnungen"

class Account(models.Model):
	name = models.CharField("Konto", max_length=200)
	type = models.CharField("Typ", max_length=1, choices=ACCOUNT_TYPE, blank=True, null=True)
	balance = models.DecimalField("Saldo", max_digits=5, decimal_places=2, blank=True, null=True)
	
	def __unicode__(self):
		return (str(self.name) + " " + str(self.balance))
	
class Account_Record(models.Model):
	amount = models.DecimalField("€", max_digits=5, decimal_places=2, blank=True, null=True)
	asset = models.OneToOneField(Account)
	liability = models.OneToOneField(Account)
	date = models.DateField()

	def __unicode__(self):
		return (str(self.liability.name) + " / " + str(self.asset.name) + " " + str(self.amount) + "€")
	

