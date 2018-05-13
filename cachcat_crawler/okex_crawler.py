from cachcat_crawler import constants
from cachcat_crawler.binance_crawler import BinanceCrawler


class OKExCrawler(BinanceCrawler):
    origin = 'okex'
    endpoint = "https://support.okex.com/hc/zh-cn/sections/115000447632?page={0}"
    page_type = constants.PageType.HTML
