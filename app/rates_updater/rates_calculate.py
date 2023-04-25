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


from app.models import Currency, Direction


def rates_calculate(direction: Direction, binance_rate: float = 100):
    currency_usd = Currency.get(Currency.name == 'USD')
    currency_rub = Currency.get(Currency.name == 'RUB')
    currency_uah = Currency.get(Currency.name == 'UAH')
    currency_usdt = Currency.get(Currency.name == 'USDT')

    if direction.currency_exchangeable == currency_usd and direction.currency_received == currency_rub:
        rate = binance_rate * 1.0355
        rate_1 = round(rate, 1)
        rate_2 = round(rate_1 + 0.1, 1)
        rate_3 = round(rate + 0.7, 1)
        rate_4 = round(rate + 1.2, 1)
        rate_5 = round(rate + 3.5, 1)
        return rate_1, rate_2, rate_3, rate_4, rate_5
    elif direction.currency_exchangeable == currency_rub and direction.currency_received == currency_usd:
        rate = binance_rate * 0.96
        rate_1 = round(rate, 1)
        rate_2 = round(rate - 0.2, 1)
        rate_3 = round(rate - 0.7, 1)
        rate_4 = round(rate - 1.2, 1)
        rate_5 = round(rate - 2.8, 1)
        return rate_1, rate_2, rate_3, rate_4, rate_5
    elif direction.currency_exchangeable == currency_uah and direction.currency_received == currency_usd:
        rate = binance_rate * 1.04
        rate_1 = round(rate, 1)
        rate_2 = round(binance_rate * 1.03571, 1)
        rate_3 = round(rate + 0.50, 1)
        rate_4 = round(rate + 1, 1)
        rate_5 = round(rate + 3, 1)
        return rate_1, rate_2, rate_3, rate_4, rate_5
    elif direction.currency_exchangeable == currency_usdt and direction.currency_received == currency_usd:
        rate_1 = 2.7
        rate_2 = 3.0
        rate_3 = 4.0
        rate_4 = 6.0
        rate_5 = 10.0
        return rate_1, rate_2, rate_3, rate_4, rate_5
