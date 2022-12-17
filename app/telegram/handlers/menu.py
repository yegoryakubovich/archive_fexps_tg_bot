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


from datetime import datetime

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.models import Customer, Order, Currency
from app.telegram import Form
from app.telegram.keyboards import kb_settings
from config import Texts, TextsKbs, TG_HELPER


async def menu(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)

    if text == TextsKbs.menu_order:
        order = Order(customer=customer, datetime=datetime.now())
        order.save()
        await Form.order.set()

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for currency in Currency.select():
            kb_btn = KeyboardButton(currency.name)
            kb.add(kb_btn)
        kb.add(TextsKbs.back)
        await message.reply(Texts.order_currency_exchangeable, reply_markup=kb)

    elif text == TextsKbs.menu_orders:
        pass
    elif text == TextsKbs.menu_settings:
        await Form.settings.set()
        await message.reply(Texts.menu_settings.format(first_name=customer.first_name,
                                                       second_name=customer.second_name), reply_markup=kb_settings)
    elif text == TextsKbs.menu_help:
        await message.reply(Texts.menu_help.format(TG_HELPER))
    else:
        await message.reply(Texts.error)
