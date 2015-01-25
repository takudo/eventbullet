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
        register_detail_page(
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

def register_detail_page(
    detail_page,
    detail_date_from_datetime_query,
    detail_date_from_ymd_query,
    detail_date_from_time_query,
    detail_date_from_format,
    detail_date_to_ymd_query,
    detail_date_to_datetime_query,
    detail_date_to_time_query,
    detail_date_to_format,
    event_title_query,
    event_description_query,
    event_tags
):
    """

    :param detail_page: DetailPage
    :param detail_date_from_ymd_query:
    :param detail_date_from_time_query:
    :param detail_date_from_format:
    :param detail_date_to_ymd_query:
    :param detail_date_to_time_query:
    :param detail_date_to_format:
    :param event_title_query:
    :param event_description_query:
    :param event_tags:
    :return:
    """

    p = detail_page

    dt_start = get_datetime_from_page(
        p,
        detail_date_from_datetime_query,
        detail_date_from_ymd_query,
        detail_date_from_time_query,
        detail_date_from_format
    )


    if detail_date_to_ymd_query is None:
        detail_date_to_ymd_query = detail_date_from_ymd_query

    dt_end = get_datetime_from_page(
        p,
        detail_date_to_datetime_query,
        detail_date_to_ymd_query,
        detail_date_to_time_query,
        detail_date_to_format
    )


    ev = Event.select().where(Event.url == p.url)
    cnt = ev.count()

    # Is already registered this event.
    if cnt == 0 :

        Event.add_event(
            p.get_text(event_title_query),
            p.url,
            event_tags,
            p.get_text(event_description_query),
            dt_start,
            dt_end
        )

    else :

        ev = ev[0]
        if ev.event_from != dt_start or ev.event_to != dt_end:
            ev.update_date(dt_start, dt_end)

def get_datetime_from_page(
    page,
    datetime_query,
    date_query,
    time_query,
    datetime_format
):
    p = page


    if datetime_query is not None:
        try:
            datetimestr = p.get_text(datetime_query)
            return datetime.datetime.strptime(datetimestr.encode("utf-8"), datetime_format)

        except:

            datetimestr = get_datetimestr_from_date_and_time_query(p, date_query, time_query)
            return datetime.datetime.strptime(datetimestr.encode("utf-8"), datetime_format)
    else :

        datetimestr = get_datetimestr_from_date_and_time_query(p, date_query, time_query)
        return datetime.datetime.strptime(datetimestr.encode("utf-8"), datetime_format)




def get_datetimestr_from_date_and_time_query(
    page,
    date_query,
    time_query
):
    p = page
    dt_end_date_str = p.get_text(date_query)
    dt_end_time_str = p.get_text(time_query)
    datetimestr = dt_end_date_str + " " + dt_end_time_str

    return datetimestr
