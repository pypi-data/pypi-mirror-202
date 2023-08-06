# -*- coding: utf-8 -*-
import os
import re
import json
import time
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的 client models。
# from tencentcloud.cvm.v20170312 import cvm_client, models
from tencentcloud.tmt.v20180321 import tmt_client, models


def translate(text, source='auto'):

    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 secretId，secretKey
        cred = credential.Credential(os.environ.get('Tencent_SecretId'), os.environ.get('Tencent_SecretKey'))

        # 实例化要请求产品（以 CVM 为例）的 client 对象
        client = tmt_client.TmtClient(cred, 'ap-shanghai')

        # 实例化一个请求对象
        req = models.TextTranslateRequest()
        req.ProjectId = 0
        req.Source = source
        req.SourceText = text
        req.Target = 'en'

        # 通过 client 对象调用想要访问的接口，需要传入请求对象
        resp = client.TextTranslate(req)
        # 输出 JSON 格式的字符串回包
        d1 = json.loads(resp.to_json_string())

        result = dict()
        result['origin'] = text
        result['source'] = d1['Source']
        result['eng'] = re.sub("[^0-9A-Za-z \u4e00-\u9fa5]", '', d1['TargetText']).lower()
        if result['source'] != 'en':
            req.SourceText = result['eng']

        req.Target = 'zh'
        resp = client.TextTranslate(req)

        d2 = json.loads(resp.to_json_string())
        result['chs'] = d2['TargetText']

        time.sleep(0.3)
        return result

    except TencentCloudSDKException as err:
        print(err)


if __name__ == '__main__':
    res = translate('PC塑料杯')
    print(res)

