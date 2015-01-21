# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq

class Page:

    def __init__(self, url):
        self.url = url
        self.pq_html = pq(url)

    def get_text(self, query, attr=None):

        elem = self.pq_elem.find(query)

        if attr is not None :
            return elem.attr(attr)
        else :
            return elem.text()



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
        elems = self.pq_html.find(query)
        return map(lambda e: DetailElem(e), elems)


class DetailElem:

    def __init__(self, elem):
        self.pq_elem = pq(elem)

    def get_detail_page(self, query, attr=None):
        return DetailPage(self.get(query, attr))


class DetailPage(Page):
    pass