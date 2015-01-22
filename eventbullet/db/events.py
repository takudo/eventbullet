# -*- coding: utf-8 -*-


from peewee import *
from playhouse.sqlite_ext import *
import datetime

db = SqliteExtDatabase("eventbullet.db")

class Event(FTSModel):

    id = PrimaryKeyAutoIncrementField()
    title = CharField()
    url = CharField(null=True)
    event_from = DateTimeField(null=True)
    evnet_to = DateTimeField(null=True)
    description = TextField(null=True)
    tags = TextField(null=True)
    updated_at = DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

db.create_tables([Event], True)
