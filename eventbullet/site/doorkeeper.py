# -*- coding: utf-8 -*-

#
# 'Doorkeeper' is Japanese event site.
# It's url is http://www.doorkeeper.jp/
#

import common

lp = common.get_list_page("http://www.doorkeeper.jp/events/")

pgs = lp.get_pagination_elems(
    "div.pagination ul li.page",
    "a",
    "href"
)

lps = map(lambda pg: pg.get_list_page(), pgs)

for lp in lps:

    detail_elems = lp.get_detail_elems()


print lp
# def notify(tag):
#
#     common.notify(
#         list_page_url="http://connpass.com/search/?q=#tag#",
#         tag=tag,
#         detail_elem_query="div.event_list",
#         detail_status_query="div.event_detail_area div.event_inner p.event_thumbnail span.label_status_event",
#         detail_status_filter=u"開催前",
#         detail_link_query="div.event_detail_area div.event_inner p.event_thumbnail a.image_link",
#         detail_link_attr="href",
#         detail_date_locale="ja_JP.utf-8",
#         detail_date_from_ymd_query="span.dtstart p.ymd",
#         detail_date_from_time_query="span.dtstart span.hi",
#         detail_date_from_format="%Y/%m/%d(%a) %H:%M",
#         # detail_date_to_ymd_query=
#         detail_date_to_datetime_query="span.dtend",
#         detail_date_to_time_query="span.dtend",
#         detail_date_to_format="%Y/%m/%d(%a) %H:%M",
#         event_title_query="h2.event_title",
#         event_description_query="div#editor_area"
#     )
#
#     print "connpass '" + tag + "' end..."

