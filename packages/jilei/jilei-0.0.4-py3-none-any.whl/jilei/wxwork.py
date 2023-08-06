import json
import requests


def group_notify(key, msg={"msgtype": "text", "text": { "content": "测试消息"}}):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'
    headers = {"Content-Type": "application/json"}
    return requests.post(url, headers=headers, data=json.dumps(msg))



