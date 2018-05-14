import datetime

from requests_html import HTML, HTMLSession

from cachcat_crawler import constants
from cachcat_crawler.crawler_base import CrawlerBase


class GateIoCrawler(CrawlerBase):
    origin = 'gateio'
    endpoint = "https://gate.io/articlelist/ann/{0}"

    page_type = constants.PageType.HTML

    def __init__(self, page=1):
        self.session = HTMLSession()
        self.session.get('https://gate.io/lang/cn')
        super(GateIoCrawler, self).__init__(page)

    def full_endpoint(self):
        return self.endpoint.format(self.page - 1)

    def is_title_needed(self, title):
        return ('开通' in title) or ('上线' in title)

    def parse_html(self):
        html = HTML(html=self.origin_request.content.decode('utf-8', 'ignore').encode('utf-8'),
                    url=self.origin_request.url)
        for item in html.find('.latnewslist'):
            url = item.absolute_links.pop()
            origin_id = int(url.split('/')[-1])
            _id = "{0}_{1}".format(self.origin, origin_id)
            title = item.find('.entry > a > h3', first=True).text.strip()
            if _id not in self.done_ids and self.is_title_needed(title):
                notice = {'id': _id, 'url': url, 'origin': constants.ORIGINS[self.origin],
                          'origin_id': origin_id, 'title': title, }
                notice_detail = HTML(html=self.session.get(url).content.decode('utf-8', 'ignore').encode('utf-8'),
                                     url=url)
                notice['content'] = notice_detail.find('.dtl-content', first=True).text
                end_index = notice['content'].index('上一篇')
                if end_index > 0:
                    notice['content'] = notice['content'][:end_index]
                notice['posted_at'] = int(
                    datetime.datetime.strptime(notice_detail.find('.new-dtl-info > span', first=True).text[:19],
                                               '%Y-%m-%d %H:%M:%S').timestamp())
                notice['short_content'] = item.find('.news-brief', first=True).text
                self.update_line(notice)
