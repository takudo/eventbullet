# -*- coding: utf-8 -*-


from peewee import *
from playhouse.sqlite_ext import *
import datetime
from pushbullet import PushBullet

import ConfigParser
import re

config = ConfigParser.RawConfigParser()
config.read('app.cfg')

db = SqliteDatabase("eventbullet.db")
api_key = config.get("pushbullet", "api_key")
title_base = config.get("pushbullet", "title")
message_base = config.get("pushbullet", "message")

pb = PushBullet(api_key)

class Event(Model):

    title = CharField()
    url = CharField(unique=True)
    event_from = DateTimeField(null=True)
    event_to = DateTimeField(null=True)
    description = TextField(null=True)
    # tags = TextField(null=True)
    notified = BooleanField(default=False) # Is notified this event
    updated_at = DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def notify(self, force=False):

        if force == True or self.notified == False:
            success, push = pb.push_note(self.event_title(), self.event_message())
            self.notified = True
            self.save()

    def event_title(self):
        return self.replace_message_tags(title_base)

    def event_message(self):
        return self.replace_message_tags(message_base)


    @staticmethod
    def add_event(title, url, tags, description=None, event_from=None, event_to=None):
        ev = Event()
        ev.title = title
        ev.url = url
        ev.description = description
        ev.save()

        for tag in tags:
            Tag.add_tag(ev, tag)

    def update_date(self, event_from=None, event_to=None):

        if event_from is not None:
            self.event_from = event_from

        if event_to is not None:
            self.event_to = event_to

        self.notified = False

        self.save()


    def replace_message_tags(self, base):
        r = base
        r = re.sub("#title#", self.title, r)
        r = re.sub("#description#", self.description, r)
        r = re.sub("#from#", (self.event_from.strftime("%Y/%m/%d %H:%M") if self.event_from is not None else "") , r)
        r = re.sub("#from_time#", (self.event_from.strftime("%H:%M") if self.event_from is not None else "") , r)
        r = re.sub("#to#", (self.event_to.strftime("%Y/%m/%d %H:%M") if self.event_to is not None else ""), r)
        r = re.sub("#to_time#", (self.event_to.strftime("%H:%M") if self.event_to is not None else ""), r)
        r = re.sub("#url#", self.url, r)
        return r

    @staticmethod
    def get_not_end_events():
        events = Event.select().where(Event.event_to > datetime.datetime.now())
        return events

class Tag(Model):

    event = ForeignKeyField(Event, related_name="event")
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    @staticmethod
    def add_tag(event, name):

        tag = Tag()
        tag.event = event
        tag.name = name
        tag.save()


db.create_tables([Event, Tag], True)

