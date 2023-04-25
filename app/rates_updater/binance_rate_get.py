#
# (c) 2023, Yegor Yakubovich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from requests import Session

from app.models import Currency


URL = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                  'Safari/537.36',
}


def binance_rate_get(currency: Currency, pay_types: list = []):
    json = {
        'proMerchantAds': False, 'page': 1, 'rows': 10, 'payTypes': pay_types, 'countries': [],
        'publisherType': 'merchant', 'asset': 'USDT',
        'fiat': currency.name, 'tradeType': 'BUY', 'transAmount': '200000'
    }

    with Session() as s:
        s.headers.update(HEADERS)
        res = s.post(URL, json=json)
        for item in res.json()['data']:
            is_merchant = True if item['advertiser']['userType'] == 'merchant' else False
            if is_merchant:
                rate = item['adv']['price']
                return float(rate)
