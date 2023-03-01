#
# (c) 2022, Yegor Yakubovich
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


from datetime import datetime, timezone, timedelta
from time import sleep

from requests import ConnectTimeout
from telebot.apihelper import ApiTelegramException
from telebot.types import InputMedia

from app.models import Direction, Currency, db, MailingRate, Rate
from app.rates_updater.binance_rate_get import binance_rate_get
from app.rates_updater.image_create import image_create
from app.rates_updater.rates_calculate import rates_calculate

from telebot import TeleBot

from config import TG_KEY, TG_GROUP_INFO, Texts, PATH_RATES_UPDATER

bot = TeleBot(TG_KEY)
MONTHS = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноябрь',
    12: 'декабрь'
}


def rates_updater():
    db.connect()
    currency_usd = Currency.get(Currency.name == 'USD')
    currency_rub = Currency.get(Currency.name == 'RUB')
    currency_uah = Currency.get(Currency.name == 'UAH')
    currency_usdt = Currency.get(Currency.name == 'USDT')
    db.close()

    while True:
        db.connect()
        directions = {}
        for direction in Direction.select():
            filename = ''
            text = ''
            if direction.currency_exchangeable == currency_rub and direction.currency_received == currency_usd:
                directions['usdrub'] = direction
                binance_rate = binance_rate_get(currency=currency_rub, pay_types=['TinkoffNew'])
                rates = rates_calculate(direction=direction, binance_rate=binance_rate)
                filename = 'usdrub'
                text = f'{rates[4]:.2f} — 100-300 usd\n' \
                       f'{rates[3]:.2f} — 300-1500 usd\n' \
                       f'{rates[2]:.2f} — 1500-5000 usd\n' \
                       f'{rates[1]:.2f} — 5000-10000 usd\n' \
                       f'{rates[0]:.2f} — от 10000 usd'
            elif direction.currency_exchangeable == currency_usd and direction.currency_received == currency_rub:
                directions['rubusd'] = direction
                binance_rate = binance_rate_get(currency=currency_rub, pay_types=['TinkoffNew'])
                rates = rates_calculate(direction=direction, binance_rate=binance_rate)
                filename = 'rubusd'
                text = f'{rates[4]:.2f} — 100-300 usd\n' \
                       f'{rates[3]:.2f} — 300-1500 usd\n' \
                       f'{rates[2]:.2f} — 1500-5000 usd\n' \
                       f'{rates[1]:.2f} — 5000-10000 usd\n' \
                       f'{rates[0]:.2f} — от 10000 usd'
                rate_1 = Rate.get(Rate.id == 1)
                rate_2 = Rate.get(Rate.id == 2)
                rate_3 = Rate.get(Rate.id == 3)
                rate_4 = Rate.get(Rate.id == 4)
                rate_5 = Rate.get(Rate.id == 5)
                rate_1.rate = rates[4] / 10000
                rate_2.rate = rates[3] / 10000
                rate_3.rate = rates[2] / 10000
                rate_4.rate = rates[1] / 10000
                rate_5.rate = rates[0] / 10000
                rate_1.save()
                rate_2.save()
                rate_3.save()
                rate_4.save()
                rate_5.save()
            elif direction.currency_exchangeable == currency_uah and direction.currency_received == currency_usd:
                directions['uahusd'] = direction
                binance_rate = binance_rate_get(currency=currency_uah, pay_types=['PrivatBank'])
                rates = rates_calculate(direction=direction, binance_rate=binance_rate)
                filename = 'uahusd'
                text = f'{rates[4]:.2f} — 100-300 usd\n' \
                       f'{rates[3]:.2f} — 300-1500 usd\n' \
                       f'{rates[2]:.2f} — 1500-5000 usd\n' \
                       f'{rates[1]:.2f} — 5000-10000 usd\n' \
                       f'{rates[0]:.2f} — от 10000 usd'
            elif direction.currency_exchangeable == currency_usdt and direction.currency_received == currency_usd:
                directions['usdtusd'] = direction
                rates = rates_calculate(direction=direction)
                filename = 'usdtusd'
                text = f'{rates[4]}% — 100-300 usd\n' \
                       f'{rates[3]}% — 300-1500 usd\n' \
                       f'{rates[2]}% — 1500-5000 usd\n' \
                       f'{rates[1]}% — 5000-10000 usd\n' \
                       f'от 15000 usd\n' \
                       f'индивидуально'

            image_create(filename=filename, text=text)

        dt_now = datetime.now(timezone.utc)
        mailing_rate = MailingRate.get_or_none((MailingRate.datetime <= dt_now) &
                                               (dt_now - timedelta(days=1) < MailingRate.datetime))
        if not mailing_rate:
            mailing_rate_datetime = datetime(year=dt_now.year, month=dt_now.month, day=dt_now.day, hour=12)
            mailing_rate = MailingRate(datetime=mailing_rate_datetime)
            mailing_rate.save()

            for name, direction in directions.items():
                image = open('{}/images/{}.png'.format(PATH_RATES_UPDATER, name), 'rb')
                message = bot.send_photo(TG_GROUP_INFO, photo=image)
                direction.message_id = message.message_id
                direction.save()

            bot.send_message(TG_GROUP_INFO, text=Texts.group_info.format(
                day=dt_now.day,
                month=MONTHS[dt_now.month]
            ), parse_mode='html')
        else:
            for name, direction in directions.items():
                image = open('{}/images/{}.png'.format(PATH_RATES_UPDATER, name), 'rb')
                try:
                    bot.edit_message_media(chat_id=TG_GROUP_INFO, message_id=direction.message_id,
                                           media=InputMedia(type='photo', media=image))
                except (ConnectTimeout, ApiTelegramException):
                    pass
                    
        db.close()
        sleep(600)
