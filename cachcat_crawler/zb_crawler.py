import datetime

from cachcat_crawler import constants
from cachcat_crawler.crawler_base import CrawlerBase


class ZbCrawler(CrawlerBase):
    origin = 'zb'
    endpoint = "https://www.zb.com/i/blog?page={0}"
    page_type = constants.PageType.HTML



    def is_title_needed(self, title):
        return '新增' in title or ('充值' in title or '交易' in title)

    def parse_html(self):
        html = self.origin_request.html
        for item in html.find('.cbp_tmtimeline > li'):
            url = item.absolute_links.pop()
            origin_id = int(url.split('item=')[-1].split('&')[0])
            _id = "{0}_{1}".format(self.origin, origin_id)
            title = item.find('header', first=True).text
            if _id not in self.done_ids and self.is_title_needed(title):
                notice = {'id': _id, 'url': url, 'origin': constants.ORIGINS[self.origin],
                          'origin_id': origin_id, 'title': title, }
                notice_detail = self.session.get(url).html
                notice['content'] = notice_detail.find('.page-content', first=True).text
                notice['posted_at'] = int(
                    datetime.datetime.strptime(item.find('time', first=True).attrs['datetime'][:19] + "+0800",
                                               '%Y-%m-%d %H:%M:%S%z').timestamp())
                notice['short_content'] = notice['content'].replace('\n', ' ')[:75] + "..."
                self.update_line(notice)
