# -*- coding: utf8 -*-
from requests_html import HTML

from cachcat_crawler.crawler_base import *


class HuobiProCrawler(CrawlerBase):
    origin = 'huobi_pro'
    endpoint = "https://www.huobipro.com/-/x/hb/p/api/contents/pro/list_notice?page={0}&limit=50&language=zh-cn"
    page_type = constants.PageType.JSON

    def notice_json_url(self, notice_id):
        return "https://www.huobipro.com/-/x/hb/p/api/contents/pro/notice/{0}".format(notice_id)

    def notice_url(self, notice_id):
        return "https://www.huobipro.com/zh-cn/notice_detail/?id={0}".format(notice_id)

    def is_title_needed(self, title):
        return '上线' in title or '开盘交易' in title

    def parse_json(self):
        origin_data = self.origin_request.json()
        for item in origin_data['data']['items']:
            _id = "{0}_{1}".format(self.origin, item['id'])
            if _id not in self.done_ids and self.is_title_needed(item['title']):
                notice = {'id': _id, 'url': self.notice_url(item['id']), 'origin': constants.ORIGINS[self.origin],
                          'origin_id': item['id'], 'posted_at': int(item['created']) / 1000,
                          'title': item['title'], 'short_content': item['content'], }
                rr = self.session.get(self.notice_json_url(item['id']))
                notice_detail = json.loads(rr.content.decode('utf-8', 'ignore'))
                print(notice_detail)
                print(rr.encoding)
                print(rr.content)
                notice['content'] = HTML(
                    html=notice_detail['data']['content']).text
                self.update_line(notice)


class HuobiHadaxCrawler(HuobiProCrawler):
    origin = 'huobi_hadax'
    endpoint = "https://content.hadax.com/p/api/contents/hadax/list_notice?page={0}&limit=50&language=zh-cn"

    def notice_json_url(self, notice_id):
        return "https://content.hadax.com/p/api/contents/hadax/notice/{0}".format(notice_id)

    def notice_url(self, notice_id):
        return "https://www.hadax.com/zh-cn/notice_detail/?id={0}".format(notice_id)
