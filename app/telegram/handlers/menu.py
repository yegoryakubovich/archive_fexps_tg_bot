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

from app.models import Customer, Order, Direction
from app.telegram import Form
from app.telegram.keyboards import kb_settings, kb_menu, kb_back
from config import Texts, TextsKbs, TG_HELPER, ORDERS_COUNT


async def handler_menu(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)

    if text == TextsKbs.menu_order:
        if Order.get_or_none((Order.customer == customer) & (Order.is_closed != True)):
            await message.reply(Texts.error_menu_order)
            return

        order = Order(customer=customer, datetime=datetime.now())
        order.save()

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for direction in Direction.select():
            kb_btn = KeyboardButton(Texts.order_direction_item.format(
                currency_exchangeable=direction.currency_exchangeable.name,
                currency_received=direction.currency_received.name
            ))
            kb.add(kb_btn)

        # No currencies with rate
        if not kb.keyboard:
            await message.reply(Texts.error_order_direction)
            return

        kb.add(TextsKbs.back)
        await Form.order.set()
        await message.reply(Texts.order_direction, reply_markup=kb)

    elif text == TextsKbs.menu_orders:
        orders = []
        for order in Order.select().where(Order.customer == customer):
            if order.doc is None:
                continue
            orders.append(order)

        if len(orders) == 0:
            await message.reply(Texts.error_orders)
            return

        orders.reverse()

        text_reply = ''
        for order in orders[:ORDERS_COUNT]:
            order: Order
            text_reply += Texts.menu_order.format(
                datetime=order.datetime, order_id='%06d' % order.id,
                currency_exchangeable_value=order.currency_exchangeable_value,
                currency_exchangeable=order.currency_exchangeable.name,
                currency_received_value=order.currency_received_value, currency_received=order.currency_received.name)
        await Form.orders.set()
        await message.reply(Texts.menu_orders.format(text_reply), reply_markup=kb_back)

    elif text == TextsKbs.menu_settings:
        await Form.settings.set()
        await message.reply(Texts.menu_settings, reply_markup=kb_settings)
    elif text == TextsKbs.menu_help:
        await message.reply(Texts.menu_help.format(TG_HELPER))
    else:
        await message.reply(Texts.error, reply_markup=kb_menu)
