import requests
import json

group_robot_webhooks = {
    "技术部": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8a301828-8d89-4fb8-b9e5-3e6f8a6a8474",
    "nnUNet-子炀PC": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f66f9b7b-685d-42af-8a64-077278422015"
}

text_msg = {
    "msgtype": "text",
    "text": {
        "content": "测试一下",
        "mentioned_list": ["朱剑波", "@all"],
        "mentioned_mobile_list": ["13850004174", "@all"]
    }
}

markdown_msg = {
    "msgtype": "markdown",
    "markdown": {
        "content": "<font color='red'>markdown</font>\n"
                   "# 一级标题\n"
                   "## 二级标题"
    }
}


def group_notify(key, msg="测试数据"):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, data=json.dumps(msg))



