# coding=UTF-8

from django.db import models

from apps._person.models import Person
from apps._accounting.models import Contract
from django.contrib.auth.models import User
import datetime

class Organisation(models.Model):
	name = models.CharField(max_length=200)


class Topic(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Thema"
		verbose_name_plural = "Themen"

class Room(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Raum"
		verbose_name_plural = "Räume"

class Category(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Fach"
		verbose_name_plural = "Fächer"

class Not_At_Event(models.Model):
	excused = models.BooleanField(default=False) # CHANGEND
	comment = models.CharField("Grund", max_length=2000, null=True)  # CHANGEND
	user = models.OneToOneField(Person)

class Event_Comment(models.Model):
	comment = models.CharField("Bewertung", max_length=2000)
	user = models.OneToOneField(Person)

	def __unicode__(self):
		return str(self.user.last_name) + " " + str(self.event.name)

class Event_Grading(models.Model):
	grading = models.CharField("Bewertung", max_length=2000)
	user = models.OneToOneField(Person)

	def __unicode__(self):
		return self.user.username

	class Meta:
		verbose_name = "Bewertung"
		verbose_name_plural = "Bewertungen"

class Event(models.Model):
	name = models.CharField("Name", max_length=200)
	date = models.DateTimeField("Tag", default=datetime.date.today)
	start_time = models.DateTimeField("Beginn", default=datetime.date.today, blank=True, null=True)
	end_time = models.DateTimeField("Ende", default=datetime.date.today, blank=True, null=True)
	room = models.OneToOneField(Room, blank=True, null=True)
	persons = models.ManyToManyField(Person, blank=True, null=True, related_name='user_participants')
	lead = models.OneToOneField(Person, blank=True, null=True,related_name='user_lead')
	category = models.OneToOneField(Category, blank=True, null=True)
	not_at_events = models.OneToOneField(Not_At_Event, blank=True, null=True, related_name='not_at_event')
	event_comments = models.ManyToManyField(Event_Comment, blank=True, null=True, related_name='event_comment')
	event_gradings = models.ManyToManyField(Event_Grading, blank=True, null=True, related_name='event_grading')
	organisation = models.OneToOneField(Organisation)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Stunde"
		verbose_name_plural = "Stunden"
		ordering = ('date', 'start_time', "category")

class Event_Series(models.Model):
	start_date = models.DateTimeField("Beginn", default=datetime.date.today, blank=True, null=True)
	end_date = models.DateTimeField("Ende", default=datetime.date.today, blank=True, null=True)
	events = models.ManyToManyField(Event, blank=True, null=True, related_name='events')

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Stundeserie"
		verbose_name_plural = "Stundeserien"

