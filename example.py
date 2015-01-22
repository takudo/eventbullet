# -*- coding: utf-8 -*-

# This example is 'conpass' (http://connpass.com/) 's data picking up.
# And searching events by keyword 'scala'.

##################
# crawling example
##################

from eventbullet.crawler.page import *

lp = ListPage(url="http://connpass.com/search/?q=scala")

urls = lp.get_detail_link_list(
    "div.event_list div.event_detail_area div.event_inner p.event_thumbnail a.image_link",
    "href"
)

elems = lp.get_elems(
    "div.event_list"
)

detail_elems = lp.get_detail_elems("div.event_list")

filterd_elems = filter(
    lambda e: e.get_text("div.event_detail_area div.event_inner p.event_thumbnail span.label_status_event") == u"開催前",
    detail_elems
)

detail_pages = map(
    lambda e: e.get_detail_page(
        "div.event_detail_area div.event_inner p.event_thumbnail a.image_link",
        "href"
    ),
    filterd_elems
)

##################
# db example
##################

from eventbullet.db.events import *

for p in detail_pages :

    cnt = Event.select().where(Event.url == p.url).count()

    if cnt == 0 :
        ev = Event()
        ev.title = p.get_text("h2.event_title")
        ev.url = p.url
        ev.tags = "scala"
        ev.description = p.get_text("div#editor_area")
        ev.save()

##################
# pushbullet
##################

evs = Event.select()

for ev in evs:
    notice

print "end..."

