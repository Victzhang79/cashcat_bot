# -*- coding: utf8 -*-
import concurrent.futures
import datetime

import leancloud
import pytz
import requests

import config
from util import *


class Sender():
    TEST_USERS = [
        "oguty0mlvZcXe6-HNSB9X-FvN6eE",
        "oguty0motG99qNtomfXT8_4Xq2Qs",
        "oguty0hBvTgD1BT3XfC_M4S9aO98",
        "oguty0sL1Q0aNPGlT54IWzQhiqVs"
    ]

    msg_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}"
    users_url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token={0}"
    leancloud.init(config.leancloud_app_id, config.leancloud_app_key)

    def __init__(self):
        if not os.path.exists("local_config"):
            os.makedirs("local_config")
        start = datetime.datetime.now().timestamp()
        access_token, _ = self.access_token()
        self.users = requests.get(self.users_url.format(access_token.strip())).json()['data']['openid']
        print("Get Users Cost:", datetime.datetime.now().timestamp() - start)

    def access_token(self):
        return tuple(open('local_config/access_token', 'r'))

    def update_access_token():
        print("Update Access Token")
        updated_at = int(datetime.datetime.now().timestamp())
        access_token = requests.get(config.wechat_access_token_url).json()['access_token']
        access_token_object = leancloud.Object.extend("Global").create_without_data('5af7b7f0a22b9d00447a5903')
        access_token_object.set('value', access_token)
        leancloud.Object.save(access_token_object)
        with open("local_config/access_token", "w") as text_file:
            text_file.write("{0}\n{1}".format(access_token, updated_at))

    def wechat_template_data(self, item, user, object_id):
        return {
            "touser": user,
            "template_id": "mcyHLEbhwG8bHFqGXPeV5AZDW68a8F_X8txHJ45IFvU",
            "url": "http://cashcat.leanapp.cn/#/messages/{0}".format(object_id),
            "miniprogram": {
                "appid": "wx0eee219b5cfcd79a",
                "pagepath": "pages/messages/show?id={0}".format(object_id)
            },
            "data": {
                "first": {
                    "value": "{0}\n".format(item['title']),
                    "color": "#ee9546"
                },
                "keyword1": {
                    "value": "{0} 交易所".format(item['origin']),
                    "color": "#777777"
                },
                "keyword2": {
                    "value": "交易所上币提醒",
                    "color": "#777777"
                },
                "keyword3": {
                    "value": datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%Y年%m月%d日 %H:%M"),
                    "color": "#777777"
                }
            }
        }

    def post_wechat(self, url, data):
        print("Start Push: ", url, data)
        res = requests.post(url, data=data)
        print("Costs", res.elapsed.total_seconds())
        return res.json()

    def send(self, item, object_id):
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.users)) as executor:
            start = datetime.datetime.now().timestamp()
            print("Start Jobs At: ", start)
            access_token, _ = self.access_token()
            jobs = {executor.submit(self.post_wechat, self.msg_url.format(access_token.strip()),
                                    json.dumps(self.wechat_template_data(item, user_id, object_id))): user_id for
                    user_id
                    in self.users}
            for future in concurrent.futures.as_completed(jobs):
                user_id = jobs[future]
                try:
                    data = future.result()
                    print(data)
                    end = datetime.datetime.now().timestamp()
                    print(user_id, " End Jobs At: ", end, "Total Cost: ", end - start)
                except Exception as exc:
                    print("Error: ", exc)
                else:
                    print("Done: ", user_id)

        return True


if __name__ == '__main__':
    Sender.update_access_token()
