import requests
import datetime
import time
from functools import wraps
import hashlib
import base64
import mimetypes


TIME_INTERVAL = 2


def now(time_fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(time_fmt)


def md5(img_binary):
    hash_md5 = hashlib.md5()
    hash_md5.update(img_binary)
    return hash_md5.hexdigest()


def get_image_b64_and_md5(image_url):
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        img_b64 = base64.b64encode(r.content).decode()
        img_md5 = md5(r.content)
        return img_b64, img_md5


def send_msg_to_group_bot(webhook_key, content, msgtype='text', max_retries=3):
    if msgtype == 'text':
        print(content)
    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}'
    headers = {'Content-Type': 'application/json'}
    data = {
        'msgtype': msgtype,
        msgtype: {'content': content}
    }
    retry = 0
    while retry < max_retries:
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 200:
            time.sleep(TIME_INTERVAL)
            return
        else:
            print(f'[{now()}] {r.status_code}: {r.json()}')
            time.sleep(5)


def send_image_to_group_bot(webhook_key, img_url, max_retries=3):
    img_b64, img_md5  = get_image_b64_and_md5(img_url)
    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}'
    headers = {'Content-Type': 'application/json'}
    data = {
        'msgtype': 'image',
        'image': {
            'base64': img_b64,
            'md5': img_md5
        }
    }
    retry = 0
    while retry < max_retries:
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 200:
            time.sleep(TIME_INTERVAL)
            return
        else:
            print(f'[{now()}] {r.status_code}: {r.json()}')
            time.sleep(5)


def wx_bot_notify(bot_key, max_retries=3):
    def inner(func):
        def wrapper(*args, **kwargs):
            retry = 0
            err = None
            resp = None
            while retry < 3:
                try:
                    ts_start = time.time()
                    resp = func(*args, **kwargs)
                    ts_use = round((time.time() - ts_start) / 60.0, 1)
                    if resp:
                        send_msg_to_group_bot(webhook_key=bot_key,
                                              msgtype='markdown',
                                              content=f"{resp.get('msg')}, 总用时: **{ts_use}** min")
                    exit()
                except Exception as e:
                    print(f'[{datetime.datetime.now()}] Error occurred when dumping data: {e}')
                    err = e
                    retry += 1
                    time.sleep(120)
            print(f'[{now()}] Reached at maximum retries.\n')
            send_msg_to_group_bot(webhook_key=bot_key,
                                  msgtype='markdown',
                                  content=f'Failed when running {func.__name__}'
                                          f'Retried {max_retries} times, Error: {str(err)}')
            return resp
        return wrapper
    return inner


def upload_media(webhook_key: str, filename, file_byte, file_type):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webhook_key}&type=file"
    headers = {}
    payload = {}
    files = [('', (filename, file_byte, file_type))]
    r = requests.request("POST", url, headers=headers, data=payload, files=files)
    d = {'media_id': None, 'errmsg': None}
    if r.status_code == 200 and r.json().get('errmsg') == 'ok':
        d['media_id'] = r.json().get('media_id')
    else:
        d['errmsg'] = f'[{now()}] Failed to upload media "{filename}", details: [{r.status_code}] {r.text}'
    return d


def send_media_to_group_bot(webhook_key, media_id):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}'
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }
    r = requests.post(url, json=data, headers=headers)
    errmsg = None
    if r.status_code == 200 and r.json().get('errmsg') == 'ok':
        print(f"[{now()}] File sent.")
    elif r.status_code != 200:
        errmsg = f'{r.status_code}: {r.text}'
    else:
        errmsg = r.json().get('errmsg')
    return errmsg


def send_file_to_group_bot(webhook_key, file_path: str):
    try:
        filename = file_path.split('/')[-1]
        filetype = mimetypes.guess_type(filename)[0]
        if not filetype:
            raise ValueError(f'Cannot get the MIMEType of file: {file_path}')
        file_byte = open(file_path, 'rb')
        res = upload_media(webhook_key, filename, file_byte, filetype)
        time.sleep(TIME_INTERVAL)
        if not res['media_id']:
            raise ValueError(f'{res["errmsg"]}')
        send_media_to_group_bot(webhook_key, res['media_id'])
        time.sleep(TIME_INTERVAL)

    except Exception as e:
        send_msg_to_group_bot(webhook_key, content=str(e))


if __name__ == '__main__':

    bot_key = '06136538-10ee-43e6-8c63-df4a9b45c6c1'
    filepath = '/Users/kevinzhu/Documents/IR replies/002044_美年健康_since2022-05-02.txt'
    errmsg = send_file_to_group_bot(webhook_key=bot_key, file_path=filepath)
