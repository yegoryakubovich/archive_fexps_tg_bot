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
from app.telegram.keyboards import kb_menu, kb_back
from config import TextsKbs, Texts, TG_HELPER


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
        await message.reply(Texts.order_currency_received, reply_markup=kb)

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
            text_reply += Texts.order_rate.format(
                num=num, currency_exchangeable_from=rate.currency_exchangeable_from,
                currency_exchangeable_to=rate.currency_exchangeable_to,
                currency_exchangeable=order.currency_exchangeable.name,
                currency_received_rate=rate.rate,
                currency_received=order.currency_received.name
            )

        await message.reply(text_reply)
        await message.answer(Texts.order_currency_exchangeable_value.format(
                currency_exchangeable=order.currency_exchangeable.name,
                currency_received=order.currency_received.name
            ), reply_markup=kb_back)
    # Enter currency exchangeable value
    elif not order.currency_exchangeable_value:
        if not text.isdigit():
            await message.reply(Texts.error_currency_value)
            return

        value = int(text)
        rate = Rate.get_or_none((Rate.currency_exchangeable == order.currency_exchangeable) &
                                (Rate.currency_received == order.currency_received) &
                                (Rate.currency_exchangeable_from <= value) &
                                (Rate.currency_exchangeable_to >= value))

        # Save changes
        order.currency_exchangeable_value = value
        order.save()

        # Errors
        if not rate:
            await message.reply(Texts.error_rate_not_exists)

            # Close order & back to menu
            order.is_closed = True
            order.save()

            await Form.menu.set()
            await message.answer(Texts.menu, reply_markup=kb_menu)
            return

        elif rate.only_admin:
            await message.reply(Texts.error_rate_only_admin.format(TG_HELPER))

            # Close order & back to menu
            order.is_closed = True
            order.save()

            await Form.menu.set()
            await message.answer(Texts.menu, reply_markup=kb_menu)
            return

        order.rate = rate.rate
        order.currency_received_value = order.currency_exchangeable_value * order.rate
        order.save()

        await message.reply(Texts.order_currency_received_value.format(
            currency_exchangeable=order.currency_exchangeable.name,
            currency_exchangeable_value=order.currency_exchangeable_value,
            currency_received=order.currency_received.name,
            currency_received_value=order.currency_received_value,
        ), reply_markup=kb_back)

    else:
        # Dev
        await message.reply(Texts.dev)

        # Close order & break menu
        order.is_closed = True
        order.save()

        await Form.menu.set()
        await message.answer(Texts.menu, reply_markup=kb_menu)
