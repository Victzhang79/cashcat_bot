from requests_html import HTMLSession
from util import *

print(load_json('data/huobi_pro.json')[-1])
s = HTMLSession()
d = s.get("https://www.huobipro.com/-/x/hb/p/api/contents/pro/notice/1528")
print(d.json())
write_json('test.json', d.json())
