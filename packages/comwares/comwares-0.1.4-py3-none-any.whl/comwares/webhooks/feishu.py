import datetime
import requests
from retry import retry
import pprint
import json
import os


class FeishuBot:

    def __init__(self, **kwargs):
        self.app_id = kwargs.get('app_id')
        self.app_secret = kwargs.get('app_secret')
        self.verification_code = kwargs.get('verification_code')
        self.tenant_access_token = None,
        self.tenant_access_token_expire_at = None
        self.sess = requests.Session()
        self.update_tenant_access_token()

    @retry(tries=3, delay=5)
    def update_tenant_access_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 200:
            d = r.json()
            self.tenant_access_token = d.get('tenant_access_token')
            self.tenant_access_token_expire_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=d['expire']-5)
            self.sess.headers['Authorization'] = f'Bearer {self.tenant_access_token}'
            print(f'[{datetime.datetime.now()}] Token updated.')
        else:
            print(f'Error {r.status_code}: {r.text}')

    def upload_img(self, image_path):
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        with open(image_path, 'rb') as f:
            image = f.read()
        r = self.sess.post(url=url, files={"image": image}, data={"image_type": "message"}, stream=True)
        # r.raise_for_status()
        if r.status_code == 200:
            data = r.json().get('data')
            image_key = data.get('image_key')
            return image_key
        else:
            print(f'Error {r.status_code}: {r.text}')

    def upload_file(self, file_path):
        url = "https://open.feishu.cn/open-apis/im/v1/files"
        file_type = file_path.split('.')[-1]
        if file_type not in ['xls', 'mp4', 'pdf', 'xls', 'ppt', 'doc', 'opus', 'stream']:
            print('Error: Unsupported file type')
            return
        with open(file_path, 'rb') as f:
            file = f.read()
        data = {
            'file_type': file_type,
            'file_name': file_path.split('/')[-1]
        }
        r = self.sess.post(url=url, files={"file": file}, data=data, stream=True)
        r.raise_for_status()
        if r.status_code == 200:
            data = r.json().get('data')
            file_key = data.get('file_key')
            return file_key
        else:
            print(f'Error {r.status_code}: {r.text}')

    def batch_send_msg(self, open_ids, msg_type, content):
        url = 'https://open.feishu.cn/open-apis/message/v4/batch_send/'
        self.sess.headers['Content-Type'] = 'application/json; charset=utf-8'
        data = {
            "open_ids": open_ids,
            "msg_type": msg_type,
            "content": content
        }
        r = self.sess.post(url, json=data)
        if r.status_code == 200 and r.json().get('code') == 0:
            print('Message sent')
        else:
            print(f'Error {r.status_code}: {r.text}')

    def send_msg(self, receive_id_type, receive_id, msg_type, content):
        url = 'https://open.feishu.cn/open-apis/im/v1/messages'
        self.sess.headers['Content-Type'] = 'application/json; charset=utf-8'
        params = {'receive_id_type': receive_id_type}
        data = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": json.dumps(content)
        }
        r = self.sess.post(url, params=params, json=data)
        if r.status_code == 200 and r.json().get('code') == 0:
            print('Message sent')
        else:
            print(f'Error {r.status_code}: {r.text}')


if __name__ == '__main__':

    app_info = {
        'app_id': os.environ.get('CHUHE_BOT_ID'),
        'app_secret': os.environ.get('CHUHE_BOT_SECRET'),
        'verification_code': os.environ.get('CHUHE_BOT_VERIFICATION_ID'),
    }
    bot = FeishuBot(**app_info)
    # file_key = bot.upload_file(file_path='../../tmp/下载.mp4')
    # file_key = 'file_v2_5c69cb1e-1b4f-44ea-9e8e-5fa6698fc6ag'
    # print('file_key: ' + file_key)
    open_ids = [
        "ou_87c7890405efd477a45d3356feb3512d",      # Kevin
        "ou_eb62dd1a408c2cc445a03291dab75420"       # YeNan
    ]
    # bot.batch_send_msg(open_ids=open_ids, msg_type='file', content={'file_key': file_key})
    # bot.send_msg(receive_id_type='open_id', receive_id=open_ids[0], msg_type='media', content={'file_key': file_key})
    img_key = bot.upload_img(image_path='tmp.png')
    print(img_key)
