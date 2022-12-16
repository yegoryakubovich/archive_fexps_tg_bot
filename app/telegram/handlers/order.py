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


from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.models import Customer, Order, Currency, Rate
from app.telegram import Form
from app.telegram.keyboards import kb_menu
from config import TextsKbs, Texts


async def hdl_order(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)
    order = Order.get((Order.customer == customer) & (Order.is_closed == False))

    # Go back
    if text == TextsKbs.back:
        # Close order & break menu
        order.is_closed = True
        order.save()

        await Form.menu.set()
        await message.reply(Texts.menu, reply_markup=kb_menu)

    # Enter currency exchangeable
    elif not order.currency_exchangeable:
        # Detect currency
        currency_exchangeable = Currency.get_or_none(Currency.name == text)
        if not currency_exchangeable:
            await message.reply(Texts.error_currency)
            return
        order.currency_exchangeable = currency_exchangeable
        order.save()

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for currency in Currency.select():
            if currency == currency_exchangeable:
                continue
            kb_btn = KeyboardButton(currency.name)
            kb.add(kb_btn)
        kb.add(TextsKbs.back)
        await message.reply(Texts.transfer_currency_received, reply_markup=kb)

    # Enter currency received
    elif not order.currency_received:
        # Detect currency
        currency_received = Currency.get_or_none(Currency.name == text)
        if not currency_received or currency_received == order.currency_exchangeable:
            await message.reply(Texts.error_currency)
            return
        order.currency_received = currency_received
        order.save()

        text_reply = ''
        for num, rate in enumerate(Rate.select().where((Rate.currency_exchangeable == order.currency_exchangeable) &
                                                       (Rate.currency_received == order.currency_received)), 1):
            text_reply += '{num}. {currency_exchangeable_from} {currency_exchangeable} - {currency_exchangeable_to} ' \
                          '{currency_exchangeable} - {currency_received_rate} {currency_received};\n' \
                .format(num=num, currency_exchangeable_from=rate.currency_exchangeable_from,
                        currency_exchangeable_to=rate.currency_exchangeable_to,
                        currency_exchangeable=order.currency_exchangeable.name,
                        currency_received_rate=rate.rate,
                        currency_received=order.currency_received.name
                        )

        await message.reply(text_reply)

        # Dev
        await message.answer(Texts.dev)

        # Close order & break menu
        order.is_closed = True
        order.save()

        await Form.menu.set()
        await message.reply(Texts.menu, reply_markup=kb_menu)

    else:
        await message.reply(Texts.error)
