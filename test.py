from requests_html import HTMLSession
from util import *

s = HTMLSession()
d = s.get("https://www.huobipro.com/-/x/hb/p/api/contents/pro/notice/1528")
print(d.json())
write_json('test.json', d.json())
