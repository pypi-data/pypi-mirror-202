from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import *
import json


# logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class CosOper:

    def __init__(self, config: dict):
        self.client = None
        self.buckets = None
        self.create_cos_client(config)
        self.update_buckets()

    def create_cos_client(self, config: dict):
        keys_must_have = ['secret_id', 'secret_key', 'region']
        for key in keys_must_have:
            if key not in config.keys():
                raise ValueError(f"Must provide '{key}'")
        config = CosConfig(SecretId=config['secret_id'],
                           SecretKey=config['secret_key'],
                           Region=config['region'],
                           Token=config.get('token'),
                           Scheme='https',
                           Proxies=config.get('proxies'))
        client = CosS3Client(config)
        self.client = client

    def update_buckets(self):
        res = self.client.list_buckets()
        buckets = res.get('Buckets')
        if isinstance(buckets, dict):
            self.buckets = buckets.get('Bucket')

    def check_bucket(self, bucket_name_keyword):
        for bucket in self.buckets:
            if bucket_name_keyword in bucket.get('Name'):
                return bucket

    def list_objects(self, bucket_name, prefix, delimiter='/', max_keys=100):
        resp = self.client.list_objects(
            Bucket=bucket_name,
            Prefix=prefix,
            Delimiter=delimiter,
            MaxKeys=max_keys,
            EncodingType='url',
        )
        return resp

    def upload_object(self, bucket_name, key, bytes_obj):
        try:
            res = self.client.put_object(Bucket=bucket_name, Key=key, Body=bytes_obj)
            return res
        except Exception as e:
            print(e)

    def is_object_exists(self, bucket_name, key):
        try:
            self.client.head_object(Bucket=bucket_name, Key=key)
            return True
        except CosServiceError:
            return False

    def get_object(self, bucket_name, key):
        pass

    def delete_object(self):
        pass

    def gen_object_url(self, bucket_name, key):
        return 'https://' + bucket_name + '.' + self.client._conf._endpoint + '/' + key


if __name__ == '__main__':

    import os
    from pprint import pprint

    config = {
        'secret_id': os.environ.get('TC_SECRET_ID'),
        'secret_key': os.environ.get('TC_SECRET_KEY'),
        'region': 'ap-shanghai'
    }

    cos = CosOper(config)
    pprint(cos.buckets)
