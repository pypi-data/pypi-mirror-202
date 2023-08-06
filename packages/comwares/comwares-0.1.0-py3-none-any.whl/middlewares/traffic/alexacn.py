import requests
import time
import datetime
from retry import retry
from pprint import pprint


class AlexaAPI:

    def __init__(self, **kwargs):
        self.api_key = kwargs.get('api_key') or '8ut2T6q6b8HKXgjTxbDAj8jlgNkFPSx0'
        self.domain = 'http://api.alexa.cn'
        self.sess = requests.Session()
        self.rank_hist = []
        self.traffic_hist = []

    @retry(tries=3, delay=10)
    def get_rank_history(self, site, start_date):
        url = self.domain + '/alexa/history'
        params = {
            'site': site,
            'key': self.api_key,
            'start': start_date,
            'range': 30
        }
        r = self.sess.get(url, params=params)
        if r.status_code == 200:
            return r.json()

    @retry(tries=3, delay=10)
    def get_traffic_history(self, site, start_date):
        url = self.domain + '/traffic/history'
        params = {
            'site': site,
            'key': self.api_key,
            'start': start_date,
            'range': 30
        }
        r = self.sess.get(url, params=params)
        if r.status_code == 200:
            return r.json()

    def get_rank_and_traffic_since(self, site: str, start_date: str):
        print(f'[{datetime.datetime.now()}] Start to get Rank & Traffic history of site: {site} since {start_date}')
        today = datetime.datetime.now()
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        while start < today:
            d = self.get_rank_history(site=site, start_date=start.strftime('%Y-%m-%d'))
            if d.get('error_code') == 0:
                self.rank_hist += d['result']
            d = self.get_traffic_history(site=site, start_date=start.strftime('%Y-%m-%d'))
            if d.get('error_code') == 0:
                self.traffic_hist += d['result']
            start += datetime.timedelta(days=30)
            time.sleep(1)
        print(f'[{datetime.datetime.now()}] Finished getting history of site: {site} since {start_date}')


if __name__ == '__main__':

    api = AlexaAPI()
    api.get_rank_and_traffic_since(site='tophatter.com', start_date='2017-01-01')


