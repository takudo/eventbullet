# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from eventbullet.crawler.page import *
from eventbullet.db.events import *
import locale

def reload(
    tags
):

    list_page_url = "https://atnd.org/events/search?q=#tag#"

    # pagination_elem_query = "div.pagination a[ref=next]"
    pagination_elem_query = "div.pagination a"
    # pagination_link_query = "a"
    pagination_link_attr = "href"

    detail_elem_query = "ul.search-result-list li"
    detail_link_query = "a.event"
    detail_link_attr = "href"

    detail_title_query="h1 a"
    detail_description_query="div#post-body"
    # detail_date_locale="ja_JP.utf-8",

    detail_date_from_datetime_query="dl.clearfix dd abbr.dtstart"
    detail_date_from_datetime_filter=None
    # detail_date_from_ymd_query="dl.clearfix dd:first-child"
    detail_date_from_ymd_query="dl.clearfix dd"
    detail_date_from_ymd_filter=u"\d\d\d\d/\d\d/\d\d"
    detail_date_from_time_query="dl.clearfix dd abbr.dtstart"
    detail_date_from_time_filter=None
    detail_date_from_format=u"%Y/%m/%d %H:%M"

    detail_date_to_datetime_query="dl.clearfix dd abbr.dtend"
    detail_date_to_datetime_filter=None
    # detail_date_to_ymd_query="dl.clearfix dd:first-child"
    detail_date_to_ymd_query="dl.clearfix dd"
    detail_date_to_ymd_filter=u"\d\d\d\d/\d\d/\d\d"
    detail_date_to_time_query="dl.clearfix dd abbr.dtend"
    detail_date_to_time_filter=None
    detail_date_to_format=u"%Y/%m/%d %H:%M"

    headers = {"Accept-Language" : "ja,en-US"}


    ##################
    # crawling
    ##################

    for tag in tags:

        print 'atnd tag:', tag

        list_page_url = list_page_url.replace("#tag#", tag)
        lp = ListPage(list_page_url)

        pagination_elems = lp.get_pagination_elems(
            pagination_elem_query,
            link_attr=pagination_link_attr
        )

        list_pages = [lp]

        if len(pagination_elems) > 0:
            list_pages.extend(map(lambda pg: pg.get_list_page(), pagination_elems))

        for lp in list_pages:

            detail_elems = lp.get_detail_elems(detail_elem_query)

            # filterd_elems = filter(
            #     lambda e: e.get_text(detail_status_query) == detail_status_filter,
            #     detail_elems
            # )

            detail_pages = map(
                lambda e: e.get_detail_page(

                    detail_link_query,
                    detail_link_attr,
                    title_query=detail_title_query,
                    description_query=detail_description_query,
                    # date_locale=detail_date_locale,
                    headers=headers,
                    date_from_datetime_query=detail_date_from_datetime_query,
                    date_from_datetime_filter=detail_date_from_datetime_filter,
                    date_from_ymd_query=detail_date_from_ymd_query,
                    date_from_ymd_filter=detail_date_from_ymd_filter,
                    date_from_time_query=detail_date_from_time_query,
                    date_from_time_filter=detail_date_from_time_filter,
                    date_from_format=detail_date_from_format,

                    date_to_datetime_query=detail_date_to_datetime_query,
                    date_to_datetime_filter=detail_date_to_datetime_filter,
                    date_to_ymd_query=detail_date_to_ymd_query,
                    date_to_ymd_filter=detail_date_to_ymd_filter,
                    date_to_time_query=detail_date_to_time_query,
                    date_to_time_filter=detail_date_to_time_filter,
                    date_to_format=detail_date_to_format

                ),
                detail_elems
            )

            print 'page count:', len(detail_pages)

            # filterd_detail_pages = filter(
            #     lambda dp: dp.is_hit_tags(tags),
            #     detail_pages
            # )

            for dp in detail_pages:
                dp.register_event([tag])


    print 'atnd end...'

