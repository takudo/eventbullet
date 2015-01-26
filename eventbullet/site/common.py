# -*- coding: utf-8 -*-
from eventbullet.crawler.page import *
from eventbullet.db.events import *
import locale

def notify(
    list_page_url,
    tag,
    detail_elem_query,
    detail_status_query,
    detail_status_filter,
    detail_link_query,
    detail_link_attr=None,
    detail_date_locale=None,
    detail_date_from_datetime_query=None,
    detail_date_from_ymd_query="",
    detail_date_from_time_query="",
    detail_date_from_format="",
    detail_date_to_datetime_query=None,
    detail_date_to_ymd_query=None,
    detail_date_to_time_query="",
    detail_date_to_format="",
    event_title_query="",
    event_description_query=""
):
    """

    :param list_page_url: String
    :param tag: String
    :return:
    """

    locale.setlocale(locale.LC_ALL, detail_date_locale)

    ##################
    # crawling
    ##################

    list_page_url = list_page_url.replace("#tag#", tag)
    lp = get_list_page(list_page_url)

    detail_elems = lp.get_detail_elems(detail_elem_query)

    filterd_elems = filter(
        lambda e: e.get_text(detail_status_query) == detail_status_filter,
        detail_elems
    )

    detail_pages = map(
        lambda e: e.get_detail_page(
            detail_link_query,
            detail_link_attr
        ),
        filterd_elems
    )

    print 'page count:', len(detail_pages)

    ##################
    # db
    ##################


    for p in detail_pages :
        p.register_detail_page(
            detail_page=p,
            detail_date_from_datetime_query=detail_date_from_datetime_query,
            detail_date_from_ymd_query=detail_date_from_ymd_query,
            detail_date_from_time_query=detail_date_from_time_query,
            detail_date_from_format=detail_date_from_format,
            detail_date_to_datetime_query=detail_date_to_datetime_query,
            detail_date_to_ymd_query=detail_date_to_ymd_query,
            detail_date_to_time_query=detail_date_to_time_query,
            detail_date_to_format=detail_date_to_format,
            event_title_query=event_title_query,
            event_description_query=event_description_query,
            event_tags=[tag]
        )


    ##################
    # pushbullet
    ##################

    evs = Event.get_not_end_events()

    for ev in evs:
        ev.notify()


def get_list_page(url):
    """

    :param url: String
    :return: ListPage
    """

    lp = ListPage(url=url)
    return lp

