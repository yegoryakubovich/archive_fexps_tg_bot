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
from aiogram.types import ParseMode

from app.models import Customer, Order
from app.telegram import Form
from app.telegram.keyboards import kb_menu
from config import Texts, TextsKbs, ORDERS_COUNT


async def handler_orders(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)

    if text == TextsKbs.back:
        await Form.menu.set()
        await message.reply(Texts.menu, reply_markup=kb_menu)
        return
    elif not text.isdigit():
        await message.reply(Texts.error_orders)
        return

    order = None
    order_id = int(text)
    orders = []
    for o in Order.select().where(Order.customer == customer):
        if o.doc is None:
            continue
        if o.id == order_id:
            order = o
        orders.append(o)
    orders.reverse()

    if order not in orders[:ORDERS_COUNT]:
        await message.reply(Texts.error_orders)
        return

    await message.reply(Texts.menu_order_details.format(
        order_id='%06d' % order.id, customer_second_name=customer.second_name, customer_first_name=customer.first_name,
        currency_exchangeable=order.currency_exchangeable.name, currency_received=order.currency_received.name,
        currency_exchangeable_value=order.currency_exchangeable_value,
        currency_received_value=order.currency_received_value, rate=order.rate,
        doc=order.doc.id, is_paid=Texts.menu_order_statuses['is_paid'][order.is_paid if order.datetime_paid else 0],
        is_completed=Texts.menu_order_statuses['is_completed'][order.is_completed],
        datetime=order.datetime if order.datetime else Texts.menu_order_statuses['datetime'][False],
        datetime_paid=order.datetime_paid if order.datetime_paid else Texts.menu_order_statuses['datetime'][False],
        datetime_completed=order.datetime_completed if order.datetime_completed else
        Texts.menu_order_statuses['datetime'][False],
        is_closed=Texts.menu_order_statuses['is_closed'][order.is_closed]

    ), parse_mode=ParseMode.HTML)
