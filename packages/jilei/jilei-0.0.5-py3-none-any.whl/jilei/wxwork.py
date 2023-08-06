import json
import requests


def group_notify(key, msg={"msgtype": "text", "text": { "content": "测试消息"}}):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'
    headers = {"Content-Type": "application/json"}
    return requests.post(url, headers=headers, data=json.dumps(msg))


def generate_nnunet_template(total_epoch, current_epoch, train_loss, val_loss, pseudo_dice, learning_rate, epoch_time, best_dice):
    """ 使用Markdown风格发送
    """
    markdown = f"# <font color='red'>NEW BEST DICE: {best_dice}!</font>\n" if best_dice else ""
    markdown = markdown + f"**Epoch No.{current_epoch}** / {total_epoch}\n"
    markdown = markdown + f"**train_loss**:     {train_loss}\n"
    markdown = markdown + f"**var_loss**:       {val_loss}\n"
    markdown = markdown + f"**pseudo_dice**:    {pseudo_dice}\n"
    markdown = markdown + f"**learning_rate**:  {learning_rate}\n"
    markdown = markdown + f"{epoch_time}s"
    return {
        "msgtype": "markdown",
        "markdown": {
            "content": markdown
            }
    }



