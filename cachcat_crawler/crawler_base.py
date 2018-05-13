from requests_html import HTMLSession

from cachcat_crawler import constants
from util import *


class CrawlerBase:
    origin = "base"
    endpoint = None
    session = None
    page = 1
    page_type = constants.PageType.Default

    def __init__(self, page=1):
        self.page = page
        self.new_items = []
        self.items = load_json(self.data_path(), default=list)
        if self.session is None:
            self.session = HTMLSession()
        self.done_ids = load_json(self.done_ids_path())
        self.prepare_path()
        self.get_origin_data()
        self.write_parsed_data()

    def done_ids_path(self):
        return "done_ids/{0}.json".format(self.origin)

    def data_path(self):
        return "data/{0}.json".format(self.origin)

    def write_parsed_data(self):
        write_json(self.data_path(), self.items)
        write_json(self.done_ids_path(), self.done_ids)

    def is_title_needed(self, title):
        return len(title) != 0

    @staticmethod
    def prepare_path():
        if not os.path.exists("done_ids"):
            os.makedirs("done_ids")
        if not os.path.exists("data"):
            os.makedirs("data")

    def get_origin_data(self):
        self.origin_request = self.session.get(self.full_endpoint())
        getattr(self, "parse_" + self.page_type)()

    # IMPLEMENT BY SUBCLASS
    def full_endpoint(self):
        return self.endpoint.format(self.page)

    # IMPLEMENT BY SUBCLASS
    def parse_json(self):
        pass

    # IMPLEMENT BY SUBCLASS
    def parse_html(self):
        pass

    def update_line(self, notice):
        self.items.append(notice)
        self.new_items.append(notice)
        self.done_ids[notice['id']] = True
