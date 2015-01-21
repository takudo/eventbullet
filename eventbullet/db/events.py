# -*- coding: utf-8 -*-


from peewee import *
from playhouse.sqlite_ext import *
import datetime

db = SqliteExtDatabase("eventbullet.db")

class Event(FTSModel):

    id = PrimaryKeyAutoIncrementField()

    title = TextField()
    updated_at = DateTimeField(default=datetime.datetime.now())
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


db.create_tables([Event], True)

ev = Event()
ev.title = "test"

ev.save()

print "end..."



