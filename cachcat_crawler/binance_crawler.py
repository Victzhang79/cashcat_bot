import datetime

from cachcat_crawler import constants
from cachcat_crawler.crawler_base import CrawlerBase


class BinanceCrawler(CrawlerBase):
    origin = 'binance'
    endpoint = "https://support.binance.com/hc/zh-cn/sections/115000106672?page={0}"
    page_type = constants.PageType.HTML

    def parse_html(self):
        html = self.origin_request.html
        for item in html.find('.article-list-item'):
            url = item.absolute_links.pop()
            origin_id = int(url.split('/')[-1].split('-')[0])
            _id = "{0}_{1}".format(self.origin, origin_id)
            if _id not in self.done_ids:
                notice = {'id': _id, 'url': url, 'origin': constants.ORIGINS[self.origin],
                          'origin_id': origin_id, 'title': item.text.strip(), }
                notice_detail = self.session.get(url).html
                notice['content'] = notice_detail.find('.article-content', first=True).text
                notice['posted_at'] = int(
                    datetime.datetime.strptime(notice_detail.find('time', first=True).attrs['datetime'],
                                               '%Y-%m-%dT%H:%M:%SZ').timestamp())
                notice['short_content'] = notice['content'].replace('\n', ' ')[:75] + "..."
                self.update_line(notice)
