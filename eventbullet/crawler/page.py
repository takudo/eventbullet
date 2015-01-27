# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import re
import locale
import datetime
from eventbullet.db.events import *
import requests

class Page:

    def __init__(self, url, headers = None):
        self.url = url

        if headers is not None:
            r = requests.get(url, headers=headers)
        else :
            r = requests.get(url)

        self.pq_html = pq(r.text)

    def get_text(self, query, attr=None):

        elem = self.pq_html.find(query)

        if attr is not None :
            return elem.attr(attr)
        else :
            return elem.text()

    def get_elems(self, query):
        elems = self.pq_html.find(query)
        return elems

    def is_relateve_path(self):
        return re.search('^\/.*', self.link)

    def get_domain(self):
        return re.search('^(http|https):\/\/(.*?)/', self.base_url).group(2)

    def get_protocol(self):
        return re.search('^(http|https):\/\/', self.base_url).group(1)

class ListPage(Page):

    def get_detail_link_list(self, query, attr=None):

        elems = self.pq_html.find(query)

        url_list = []

        if attr is not None :
            for elem in elems:
                pq_elem = pq(elem)
                url_list.append(pq_elem.attr(attr))

        else :
            for elem in elems:
                url_list.append(elem.text())

        return url_list

    def get_detail_elems(self, query):
        return map(lambda e: DetailElem(e, self.url), self.get_elems(query))

    def get_pagination_elems(self, elem_query, link_query=None, link_attr=None):

        # return self.get_elems(query)
        return map(lambda e: PaginationElem(self.url, e, link_query, link_attr), self.get_elems(elem_query))

class PaginationElem(Page):

    def __init__(
            self,
            url,
            elem,
            link_query=None,
            link_attr=None
    ):
        self.base_url = url
        self.pq_html = pq(elem)
        self.link_query = link_query
        self.link_attr = link_attr

        if link_query is not None:
            link_elem = self.pq_html.find(link_query)
        else :
            link_elem = pq(elem)

        if link_attr is not None:
            self.link = link_elem.attr(link_attr)
        else :
            self.link = link_elem.text()

        if self.is_relateve_path():

            domain = self.get_domain()
            protocol = self.get_protocol()
            self.link = protocol + "://" + domain + self.link

        else:
            self.link = self.base_url + self.link


    def get_list_page(self, headers=None):
        return ListPage(self.link, headers=headers)

class DetailElem(Page):

    def __init__(self, elem, base_url=None):
        self.pq_html = pq(elem)
        self.base_url = base_url

    def get_detail_page(
            self,
            query,
            attr=None,
            title_query="",
            description_query="",
            date_locale="ja_JP.utf-8",
            headers = None,
            date_from_datetime_query=None,
            date_from_datetime_filter=None,
            date_from_ymd_query=None,
            date_from_ymd_filter=None,
            date_from_time_query=None,
            date_from_time_filter=None,
            date_from_format=None,
            date_to_datetime_query=None,
            date_to_datetime_filter=None,
            date_to_ymd_query=None,
            date_to_ymd_filter=None,
            date_to_time_query=None,
            date_to_time_filter=None,
            date_to_format=None
    ):
        """

        :param query:
        :param attr:
        :param title_query:
        :param description_query:
        :param date_locale:
        :param date_from_datetime_query:
        :param date_from_datetime_filter:
        :param date_from_ymd_query:
        :param date_from_ymd_filter:
        :param date_from_time_query:
        :param date_from_time_filter:
        :param date_from_format:
        :param date_to_datetime_query:
        :param date_to_datetime_filter:
        :param date_to_ymd_query:
        :param date_to_ymd_filter:
        :param date_to_time_query:
        :param date_to_time_filter:
        :param date_to_format:
        :return: DetailPage
        """

        self.link = self.get_text(query, attr)
        if self.is_relateve_path():
            domain = self.get_domain()
            protocol = self.get_protocol()
            self.link = protocol + "://" + domain + self.link
        else:
            self.link = self.base_url + self.link

        return DetailPage(
            self.link,
            title_query=title_query,
            description_query=description_query,
            date_locale=date_locale,
            headers = headers,
            date_from_datetime_query=date_from_datetime_query,
            date_from_datetime_filter=date_from_datetime_filter,
            date_from_ymd_query=date_from_ymd_query,
            date_from_ymd_filter=date_from_ymd_filter,
            date_from_time_query=date_from_time_query,
            date_from_time_filter=date_from_time_filter,
            date_from_format=date_from_format,
            date_to_datetime_query=date_to_datetime_query,
            date_to_datetime_filter=date_to_datetime_filter,
            date_to_ymd_query=date_to_ymd_query,
            date_to_ymd_filter=date_to_ymd_filter,
            date_to_time_query=date_to_time_query,
            date_to_time_filter=date_to_time_filter,
            date_to_format=date_to_format
        )


class DetailPage(Page):

    def __init__(
            self,
            url,
            title_query,
            description_query,
            date_locale,
            headers = None,
            date_from_datetime_query=None,
            date_from_datetime_filter=None,
            date_from_ymd_query=None,
            date_from_ymd_filter=None,
            date_from_time_query=None,
            date_from_time_filter=None,
            date_from_format=None,
            date_to_datetime_query=None,
            date_to_datetime_filter=None,
            date_to_ymd_query=None,
            date_to_ymd_filter=None,
            date_to_time_query=None,
            date_to_time_filter=None,
            date_to_format=None
    ):
        """

        :param url: String
        :param title_query: String
        :param description_query: String
        :param date_locale: String
        :param date_from_datetime_query: String
        :param date_from_datetime_filter: String
        :param date_from_ymd_query: String
        :param date_from_ymd_filter: String
        :param date_from_time_query: String
        :param date_from_time_filter: String
        :param date_from_format: String
        :param date_to_datetime_query: String
        :param date_to_datetime_filter: String
        :param date_to_ymd_query: String
        :param date_to_ymd_filter: String
        :param date_to_time_query: String
        :param date_to_time_filter: String
        :param date_to_format: String
        :return:
        """

        self.url = url
        # self.pq_html = pq(url)

        if headers is not None:
            r = requests.get(url, headers=headers)
        else :
            r = requests.get(url)

        self.pq_html = pq(r.text)


        self.title = self.get_text(title_query)
        self.description = self.get_text(description_query)
        self.date_locate = date_locale

        self.date_from_datetime_query = date_from_datetime_query
        self.date_from_datetime_filter = date_from_datetime_filter
        self.date_from_ymd_query = date_from_ymd_query
        self.date_from_ymd_filter = date_from_ymd_filter
        self.date_from_time_query = date_from_time_query
        self.date_from_time_filter = date_from_time_filter
        self.date_from_format = date_from_format
        self.date_to_datetime_query = date_to_datetime_query
        self.date_to_datetime_filter = date_to_datetime_filter
        self.date_to_ymd_query = date_to_ymd_query
        self.date_to_ymd_filter = date_to_ymd_filter
        self.date_to_time_query = date_to_time_query
        self.date_to_time_filter = date_to_time_filter
        self.date_to_format = date_to_format

        self.tags = []

    def is_hit_tags(self, tags):
        for tag in tags:
            if self.is_hit_tag(tag) :
                self.tags.append(tag)

        return len(self.tags) > 0

    def is_hit_tag(self, tag):
        # return re.search('^(http|https):\/\/(.*?)/', self.base_url).group(2)
        #
        return self.title.find(tag) > 0 or self.description.find(tag) > 0

    def register_event(
        self,
        event_tags
    ):
        """
        :param event_tags:
        :return:
        """

        try:

            dt_start = DetailPage.get_datetime_from_page(
                self,
                self.date_from_datetime_query,
                self.date_from_datetime_filter,
                self.date_from_ymd_query,
                self.date_from_ymd_filter,
                self.date_from_time_query,
                self.date_from_time_filter,
                self.date_from_format
            )

            if self.date_to_ymd_query is None:
                self.date_to_ymd_query = self.date_from_ymd_query

            dt_end = DetailPage.get_datetime_from_page(
                self,
                self.date_to_datetime_query,
                self.date_to_datetime_filter,
                self.date_to_ymd_query,
                self.date_to_ymd_filter,
                self.date_to_time_query,
                self.date_to_time_filter,
                self.date_to_format
            )

            ev = Event.select().where(Event.url == self.url)
            cnt = ev.count()

            # Is already registered this event.
            if cnt == 0 :

                Event.add_event(
                    self.title,
                    self.url,
                    event_tags,
                    self.description,
                    dt_start,
                    dt_end
                )

            else :

                ev = ev[0]
                if ev.event_from != dt_start or ev.event_to != dt_end:
                    ev.update_date(dt_start, dt_end)

        except Exception as e:
            print "event url:", self.url, "error:", e.message, e

    @staticmethod
    def get_datetime_from_page(
            page,
            datetime_query = None,
            datetime_filter = None,
            date_query = None,
            date_filter = None,
            time_query = None,
            time_filter = None,
            datetime_format = None
    ):
        """

        :param datetime_query:
        :param date_query:
        :param time_query:
        :param datetime_format:
        :return:
        """
        page
        if datetime_query is not None:
            try:
                datetimestr = page.get_text(datetime_query)

                if datetime_filter is not None:
                    datetimestr = re.search(datetime_filter, datetimestr).group(0)

                return datetime.datetime.strptime(datetimestr.encode("utf-8"), datetime_format)

            except:

                datetimestr = DetailPage.get_datetimestr_from_date_and_time_query(
                    page,
                    date_query,
                    date_filter,
                    time_query,
                    time_filter
                )
                return datetime.datetime.strptime(datetimestr.encode("utf-8"), datetime_format)
        else :

            datetimestr = DetailPage.get_datetimestr_from_date_and_time_query(
                page,
                date_query,
                date_filter,
                time_query,
                time_filter
            )
            return datetime.datetime.strptime(datetimestr.encode("utf-8"), datetime_format)


    @staticmethod
    def get_datetimestr_from_date_and_time_query(
            page,
            date_query,
            date_filter,
            time_query,
            time_filter
    ):
        p = page
        date_str = p.get_text(date_query)
        if date_filter is not None:

            m = re.search(date_filter, date_str)
            if m is not None:
                date_str = m.group(0)

        time_str = p.get_text(time_query)
        if time_filter is not None:
            # time_str = re.search(time_filter, time_str).group(0)
            m = re.search(time_filter, time_str)
            if m is not None:
                time_str = m.group(0)

        datetimestr = date_str + " " + time_str

        return datetimestr
