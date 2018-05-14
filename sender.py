# -*- coding: utf8 -*-
import concurrent.futures
import datetime

import leancloud
import pytz
import requests

import config
from util import *


class Sender():
    USERS = [
        # "oguty0mlvZcXe6-HNSB9X-FvN6eE",
        "oguty0motG99qNtomfXT8_4Xq2Qs",
        # "oguty0hBvTgD1BT3XfC_M4S9aO98",
        # "oguty0sL1Q0aNPGlT54IWzQhiqVs"
    ]

    msg_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}"

    def __init__(self):
        if not os.path.exists("local_config"):
            os.makedirs("local_config")
        leancloud.init(config.leancloud_app_id, config.leancloud_app_key)

    def access_token(self):
        return tuple(open('local_config/access_token', 'r'))

    def update_access_token(self):
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
        return res.json()

    def send(self, item, object_id):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            access_token, _ = self.access_token()
            jobs = {executor.submit(self.post_wechat, self.msg_url.format(access_token.strip()),
                                    json.dumps(self.wechat_template_data(item, user_id, object_id))): user_id for
                    user_id
                    in self.USERS}
            for future in concurrent.futures.as_completed(jobs):
                user_id = jobs[future]
                try:
                    data = future.result()
                    print(data)
                except Exception as exc:
                    print("Error: ", exc)
                else:
                    print("Done: ", user_id)

        return True


if __name__ == '__main__':
    sender = Sender()
    sender.update_access_token()
