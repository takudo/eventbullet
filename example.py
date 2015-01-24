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
import locale
import datetime

locale.setlocale(locale.LC_ALL, "ja_JP")

for p in detail_pages :

    dt_start_date_str = p.get_text("span.dtstart p.ymd")
    dt_start_time_str = p.get_text("span.dtstart span.hi")
    datetimestr = dt_start_date_str + " " + dt_start_time_str
    dt_start = datetime.datetime.strptime(datetimestr.encode("utf-8"), "%Y/%m/%d(%a) %H:%M" )

    dt_end_date_str = dt_start_date_str
    dt_end_time_str = p.get_text("span.dtend")
    datetimestr = dt_end_date_str + " " + dt_end_time_str
    dt_end = datetime.datetime.strptime(datetimestr.encode("utf-8"), "%Y/%m/%d(%a) %H:%M" )

    ev = Event.select().where(Event.url == p.url)
    cnt = ev.count()

    # Is already registered this event.
    if cnt == 0 :

        Event.add_event(
            p.get_text("h2.event_title"),
            p.url,
            ["scala"],
            p.get_text("div#editor_area"),
            dt_start,
            dt_end
        )

    else :

        ev = ev[0]
        if ev.event_from != dt_start or ev.event_to != dt_end:
            ev.update_date(dt_start, dt_end)

##################
# pushbullet
##################

evs = Event.get_not_end_events()

for ev in evs:
    ev.notify(force=True)

print "end..."

