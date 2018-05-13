import datetime

import leancloud
import pytz
import requests

import config
from util import *


class Sender():
    USERS = ["oguty0mlvZcXe6-HNSB9X-FvN6eE",
             "oguty0motG99qNtomfXT8_4Xq2Qs",
             "oguty0hBvTgD1BT3XfC_M4S9aO98",
             "oguty0sL1Q0aNPGlT54IWzQhiqVs"]

    def __init__(self):
        if not os.path.exists("local_config"):
            os.makedirs("local_config")
        leancloud.init(config.leancloud_app_id, config.leancloud_app_key)

    def access_token(self):
        return tuple(open('local_config/access_token', 'r'))

    def update_access_token(self):
        _, last_updated_at = self.access_token()
        if int(datetime.datetime.now().timestamp()) >= int(last_updated_at) + 7200:
            print("Update Access Token")
            access_token_object = leancloud.Query("Global").equal_to("name", "AccessToken").find()[0]
            updated_at = int(access_token_object.updated_at.timestamp())
            access_token = json.loads(access_token_object.get('value'))['access_token']
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

    def send(self, item, object_id):
        access_token, _ = self.access_token()
        # for user_id in self.USERS:
        #     template_data = self.wechat_template_data(item, user_id, object_id)
        #     requests.post(
        #         "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}".format(access_token.strip()),
        #         data=json.dumps(template_data))
        template_data = self.wechat_template_data(item, self.USERS[1], object_id)
        requests.post(
            "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}".format(access_token.strip()),
            data=json.dumps(template_data))
        return True


if __name__ == '__main__':
    sender = Sender()
    sender.update_access_token()
