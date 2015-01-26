# -*- coding: utf-8 -*-

#
# 'Doorkeeper' is Japanese event site.
# It's url is http://www.doorkeeper.jp/
#

import common

def notify(tags):

    list_page_url = "http://www.doorkeeper.jp/events/"
    pagination_elem_query = "div.pagination ul li.page"
    pagination_link_query = "a"
    pagination_link_attr = "href"

    detail_elem_query = "div.row-fluid"
    detail_link_query = "div.span11 div.large a"
    detail_link_attr = "href"

    detail_title_query="h1.client-main-title"
    detail_description_query="div#description"
    # detail_date_locale="ja_JP.utf-8",

    detail_date_from_datetime_query="div.client-main-date"
    detail_date_from_ymd_query=None
    detail_date_from_ymd_filter=None
    detail_date_from_time_query=None
    detail_date_from_time_filter=None
    # detail_date_from_format="2015-02-01（日）14:00 - 17:00",

    detail_date_from_datetime_filter=u'^\d\d\d\d\-\d\d\-\d\d（.）\d\d:\d\d'
    detail_date_from_format=u"%Y-%m-%d（%a）%H:%M - %H:%M"

    detail_date_to_datetime_query="div.client-main-date"
    detail_date_to_datetime_filter=None
    detail_date_to_ymd_query=u"%Y-%m-%d（%a）%H:%M - %H:%M"
    detail_date_to_ymd_filter=u'^\d\d\d\d\-\d\d\-\d\d（.）'
    detail_date_to_time_query=u"%Y-%m-%d（%a）%H:%M - %H:%M"
    detail_date_to_time_filter=u"\d\d:\d\d$"
    detail_date_to_format=u"%Y-%m-%d（%a） %H:%M"


    lp = common.get_list_page(list_page_url)

    pgs = lp.get_pagination_elems(
        pagination_elem_query,
        pagination_link_query,
        pagination_link_attr
    )

    lps = map(lambda pg: pg.get_list_page(), pgs)

    for lp in lps:

        detail_elems = lp.get_detail_elems(detail_elem_query)

        # detail_pages = map(lambda de: de.get_detail_page(
        #     detail_link_query,
        #     detail_link_attr,
        #     title_query=detail_title_query,
        #     description_query=detail_description_query,
        #     # date_locale=detail_date_locale,
        #     date_from_datetime_query=detail_date_from_datetime_query,
        #     date_from_ymd_query=detail_date_from_ymd_query,
        #     date_from_time_query=detail_date_from_time_query,
        #     date_from_format=detail_date_from_format,
        #     date_to_datetime_query=detail_date_to_datetime_query,
        #     date_to_ymd_query=detail_date_to_ymd_query,
        #     date_to_time_query=detail_date_to_time_query,
        #     date_to_format=detail_date_to_format
        # ), detail_elems)
        #
        #
        # filterd_detail_pages = filter(
        #     lambda dp: dp.is_hit_keywords(tags),
        #     detail_pages
        # )



        detail_page = detail_elems[0].get_detail_page(
            detail_link_query,
            detail_link_attr,
            title_query=detail_title_query,
            description_query=detail_description_query,
            # date_locale=detail_date_locale,
            date_from_datetime_query=detail_date_from_datetime_query,
            date_from_ymd_query=detail_date_from_ymd_query,
            date_from_time_query=detail_date_from_time_query,
            date_from_filter=detail_date_from_filter,
            date_from_format=detail_date_from_format,
            date_to_datetime_query=detail_date_to_datetime_query,
            date_to_ymd_query=detail_date_to_ymd_query,
            date_to_time_query=detail_date_to_time_query,
            date_to_filter=detail_date_to_filter,
            date_to_format=detail_date_to_format
        )

        print detail_page.is_hit_tags([u"ヨガ"])

        detail_page.register_event(detail_page.tags)

    print lp
