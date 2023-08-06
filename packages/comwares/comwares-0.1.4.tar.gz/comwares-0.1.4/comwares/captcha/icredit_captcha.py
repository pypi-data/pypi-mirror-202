import requests
import urllib.parse as parse
import base64
import os
from comwares import change_to_root_dir
from PIL import Image


def verify_captcha(img_filename, appcode=None):
    endpoint = 'https://codevirify.market.alicloudapi.com/icredit_ai_image/verify_code/v1'
    appcode = appcode or os.environ.get('icredit_appcode')
    if appcode is None:
        raise ValueError('Please provide valid iCredit appcode in ENV before using this func.')
    headers = {
        'Authorization': 'APPCODE ' + appcode,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    fp = open(img_filename, 'rb')
    contents = base64.b64encode(fp.read())
    fp.close()
    data = {'IMAGE': contents, 'IMAGE_TYPE': '0'}
    data = parse.urlencode(data).encode('UTF-8')
    r = requests.post(url=endpoint, data=data, headers=headers)
    return process_resp(r)


def process_resp(resp):
    if resp.status_code == 200:
        code = resp.json().get('VERIFY_CODE_ENTITY').get('VERIFY_CODE')
        return code
    else:
        s = 'Failed: {code} - {msg}'.format(code=resp.status_code, msg=resp.text)
        print(s)
        return None


if __name__ == '__main__':
    change_to_root_dir('merchant')
    img_filename = 'tmp/captcha_imgs/wishpost/raw/1593326608.png'
    img = Image.open(img_filename)
    captcha = verify_captcha(img_filename, appcode='a8fec07ce8754450889c78a71b25a993')
    print('Captcha: ', captcha)
