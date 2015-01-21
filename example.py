# -*- coding: utf-8 -*-

# This example is 'conpass' (http://connpass.com/) 's data picking up.
# And searching events by keyword 'scala'.

from eventbullet.crawler.page import *

lp = ListPage(url="http://connpass.com/search/?q=scala")

urls = lp.get_detail_link_list(
    "div.event_list div.event_detail_area div.event_inner p.event_thumbnail a.image_link",
    "href")

elems = lp.get_detail_elems(
    "div.event_list"
)

filterd_elems = filter(
    lambda e: e.get_text("div.event_detail_area div.event_inner p.event_thumbnail span.label_status_event") == u"開催前",
    elems
)

print "end..."